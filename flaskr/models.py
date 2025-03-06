# from app import db

# class Test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)

#     def __repr__(self):
#         return f"<Task {self.title}>"



# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata


from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.sql import func
from uuid import UUID
import datetime
from database import Base

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

    #To Do - Assign current timestamp in modified at column
    def __init__(self, task_title=None,task_description=None,modified_on=None,priority_id=None,planned_start_date=None,planned_end_date=None,status_id=None,completed_on=None):
        self.task_title = task_title
        self.task_description = task_description
        self.modified_on = modified_on
        self.priority_id = priority_id
        self.planned_start_date = planned_start_date
        self.planned_end_date = planned_end_date
        self.status_id = status_id
        self.completed_on = completed_on
    
    def __repr__(self):
        return f'<Task ID: {self.id!r}, Task: task_title = {self.task_title!r} >'

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

    def __init__(self, task_id=None, child_task_id=None, modified_on=None, order=None):
        self.task_id = task_id
        self.child_task_id = child_task_id
        self.modified_on = modified_on
        self.order = order
    
    def __repr__(self):
        return f'<Parent Task: {self.task_id!r}, Child Task: {self.child_task_id!r}>'
    
class TaskStatusLogs(Base):
    __tablename__ = "task_status_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_id = mapped_column(ForeignKey("master_to_do_list.id"))
    status_id = mapped_column(ForeignKey("task_status_types.id"))
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    task = relationship("MasterToDoList")
    status = relationship("TaskStatusTypes")

    def __init__(self,task_id=None, status_id=None):
        self.task_id = task_id
        self.status_id = status_id
    
    def __repr__(self):
        return f'<Task: {self.task_id!r}, Status Log: {self.status_id!r}'

class TaskStatusTypes(Base):
    __tablename__ = "task_status_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    status_description: Mapped[str] = mapped_column(String(255))

    def __init__(self,status=None,status_description=None):
        self.status = status
        self.status_description = status_description
    
    def __repr__(self):
        return f'<Status ID: {self.status_id!r}, Status: {self.status!r}>'

class TaskPriorityTypes(Base):
    __tablename__ = "task_priority_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[str] = mapped_column(String(50))
    priority_description: Mapped[str] = mapped_column(String(255))

    def __init__(self,priority=None,priority_description=None):
        self.priority = priority
        self.priority_description = priority_description
    
    def __repr__(self):
        return f'<Priority ID: {self.priority_id!r}, Priority: {self.priority!r}>'

