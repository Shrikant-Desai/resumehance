from datetime import datetime
from sqlalchemy import Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.db.connection import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    raw_text: Mapped[str] = mapped_column(Text)
    parsed_json: Mapped[dict] = mapped_column(JSON)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    skill_vectors: Mapped[list["SkillVector"]] = relationship(back_populates="resume")
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="resume")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text)
    parsed_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    skill_vectors: Mapped[list["SkillVector"]] = relationship(
        back_populates="job_description"
    )
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="job_description")


class SkillVector(Base):
    __tablename__ = "skill_vectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_name: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(10))  # "resume" or "jd"
    resume_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("resumes.id"), nullable=True
    )
    jd_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("job_descriptions.id"), nullable=True
    )
    vector: Mapped[list] = mapped_column(
        Vector(768)
    )  # 768 dims for Google embedding model

    resume: Mapped["Resume | None"] = relationship(
        back_populates="skill_vectors", foreign_keys=[resume_id]
    )
    job_description: Mapped["JobDescription | None"] = relationship(
        back_populates="skill_vectors", foreign_keys=[jd_id]
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"))
    jd_id: Mapped[int] = mapped_column(Integer, ForeignKey("job_descriptions.id"))
    match_result: Mapped[dict] = mapped_column(JSON)
    gap_result: Mapped[dict] = mapped_column(JSON)
    readiness_score: Mapped[float] = mapped_column(Float)
    roadmap: Mapped[dict] = mapped_column(JSON)
    result_json: Mapped[dict] = mapped_column(JSON)  # full response cached here
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    resume: Mapped["Resume"] = relationship(back_populates="analyses")
    job_description: Mapped["JobDescription"] = relationship(back_populates="analyses")
