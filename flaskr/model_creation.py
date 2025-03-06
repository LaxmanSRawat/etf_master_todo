
# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy import create_engine,String, Integer, ForeignKey
from sqlalchemy.sql import func
from uuid import UUID
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

class MasterToDoList(Base):
    __tablename__ = "master_to_do_list"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_title: Mapped[str]= mapped_column(String(255))
    task_description: Mapped[str] = mapped_column(String(500))
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    modified_on: Mapped[Optional[datetime.datetime]]
    priority_id = mapped_column(ForeignKey("task_priority_types.id"))
    planned_start_date: Mapped[Optional[datetime.datetime]]
    planned_end_date: Mapped[Optional[datetime.datetime]]
    status_id = mapped_column(ForeignKey("task_status_types.id"))
    completed_on: Mapped[Optional[datetime.datetime]]

    status = relationship("TaskStatusTypes")
    priority = relationship("TaskPriorityTypes")

class ChildTaskMapping(Base):
    __tablename__ = "child_task_mapping"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_id = mapped_column(ForeignKey("master_to_do_list.id"))
    child_task_id = mapped_column(ForeignKey("master_to_do_list.id"))
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    modified_on:  Mapped[Optional[datetime.datetime]]
    order: Mapped[int]

    parent_task = relationship("MasterToDoList", foreign_keys= [task_id])
    child_task = relationship("MasterToDoList", foreign_keys=[child_task_id])

class TaskStatusLogs(Base):
    __tablename__ = "task_status_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_id = mapped_column(ForeignKey("master_to_do_list.id"))
    status_id = mapped_column(ForeignKey("task_status_types.id"))
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    task = relationship("MasterToDoList")
    status = relationship("TaskStatusTypes")

class TaskStatusTypes(Base):
    __tablename__ = "task_status_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    status_description: Mapped[str] = mapped_column(String(255))

class TaskPriorityTypes(Base):
    __tablename__ = "task_priority_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[str] = mapped_column(String(50))
    priority_description: Mapped[str] = mapped_column(String(255))



engine = create_engine(os.getenv("DATABASE_URL"), echo = True)

Base.metadata.create_all(engine)
