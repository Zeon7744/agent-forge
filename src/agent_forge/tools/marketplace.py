# -*- coding: utf-8 -*-
"""
工具市场模块 - Skills 注册表与分发
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import hashlib
import json
from pathlib import Path


@dataclass
class SkillMeta:
    """Skill 元数据"""
    skill_id: str
    name: str
    description: str
    version: str
    author: str
    tags: List[str]
    downloads: int = 0
    rating: float = 0.0
    reviews: int = 0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    is_verified: bool = False
    price: float = 0.0  # 0 = 免费
    license_type: str = "MIT"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "downloads": self.downloads,
            "rating": self.rating,
            "reviews": self.reviews,
            "price": self.price,
            "license_type": self.license_type,
            "is_verified": self.is_verified,
        }


class Marketplace:
    """工具市场 - Skills 注册表与分发"""
    
    def __init__(self, storage_path: str = "./marketplace"):
        self._storage_path = Path(storage_path)
        self._storage_path.mkdir(parents=True, exist_ok=True)
        self._skills: Dict[str, SkillMeta] = {}
        self._load_index()
    
    def _index_path(self) -> Path:
        return self._storage_path / "index.json"
    
    def _load_index(self):
        """加载索引"""
        if self._index_path().exists():
            try:
                data = json.loads(self._index_path().read_text())
                for item in data:
                    self._skills[item["skill_id"]] = SkillMeta(**item)
            except:
                pass
    
    def _save_index(self):
        """保存索引"""
        data = [s.to_dict() for s in self._skills.values()]
        self._index_path().write_text(json.dumps(data, ensure_ascii=False, indent=2))
    
    def register(self, skill: SkillMeta) -> str:
        """注册 Skill"""
        self._skills[skill.skill_id] = skill
        self._save_index()
        return skill.skill_id
    
    def list(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        verified: bool = False,
        free_only: bool = False,
        sort: str = "downloads",
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """列出 Skills（支持筛选和分页）"""
        skills = list(self._skills.values())
        
        # 筛选
        if category:
            skills = [s for s in skills if s.category == category]
        if tag:
            skills = [s for s in skills if tag in s.tags]
        if verified:
            skills = [s for s in skills if s.is_verified]
        if free_only:
            skills = [s for s in skills if s.price == 0]
        
        # 排序
        if sort == "downloads":
            skills.sort(key=lambda x: x.downloads, reverse=True)
        elif sort == "rating":
            skills.sort(key=lambda x: x.rating, reverse=True)
        elif sort == "newest":
            skills.sort(key=lambda x: x.created_at, reverse=True)
        
        # 分页
        total = len(skills)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = skills[start:end]
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "skills": [s.to_dict() for s in paginated],
        }
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索 Skills（简单关键词匹配）"""
        query_lower = query.lower()
        results = []
        for skill in self._skills.values():
            score = 0
            if query_lower in skill.name.lower():
                score += 10
            if query_lower in skill.description.lower():
                score += 5
            if any(query_lower in tag.lower() for tag in skill.tags):
                score += 3
            if score > 0:
                results.append((score, skill.to_dict()))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]
    
    def get(self, skill_id: str) -> Optional[Dict]:
        """获取 Skill 详情"""
        skill = self._skills.get(skill_id)
        if skill:
            skill.downloads += 1
            self._save_index()
            return skill.to_dict()
        return None
    
    def download(self, skill_id: str, target_dir: str = ".") -> Optional[str]:
        """下载并安装 Skill"""
        skill = self._skills.get(skill_id)
        if not skill:
            return None
        
        skill.downloads += 1
        self._save_index()
        
        # 简化版：返回下载路径（实际需要下载文件）
        install_path = Path(target_dir) / skill_id
        install_path.mkdir(parents=True, exist_ok=True)
        (install_path / "SKILL.md").write_text(
            f"# {skill.name}\n\n{skill.description}\n\n"
            f"版本: {skill.version}\n"
            f"作者: {skill.author}\n"
            f"许可证: {skill.license_type}"
        )
        return str(install_path)
    
    def verify_skill(self, skill_id: str, verified: bool = True) -> bool:
        """验证/撤销验证"""
        skill = self._skills.get(skill_id)
        if skill:
            skill.is_verified = verified
            skill.updated_at = time.time()
            self._save_index()
            return True
        return False
    
    def add_review(self, skill_id: str, rating: float, comment: str = "") -> Dict:
        """添加评价"""
        skill = self._skills.get(skill_id)
        if not skill:
            return {"error": "Skill not found"}
        
        # 更新评分
        total_rating = skill.rating * skill.reviews + rating
        skill.reviews += 1
        skill.rating = total_rating / skill.reviews
        
        self._save_index()
        return {
            "skill_id": skill_id,
            "rating": skill.rating,
            "reviews": skill.reviews,
        }
    
    def stats(self) -> Dict:
        """市场统计"""
        total = len(self._skills)
        verified = sum(1 for s in self._skills.values() if s.is_verified)
        free = sum(1 for s in self._skills.values() if s.price == 0)
        paid = total - free
        total_downloads = sum(s.downloads for s in self._skills.values())
        
        return {
            "total_skills": total,
            "verified_skills": verified,
            "free_skills": free,
            "paid_skills": paid,
            "total_downloads": total_downloads,
        }
