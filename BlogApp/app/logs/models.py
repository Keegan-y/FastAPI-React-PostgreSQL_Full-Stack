from sqlalchemy import Column, Integer, String,DateTime
import sys

sys.path.append("..")
from logs.dbconf import Base


# Log Model
class ProcessLog(Base):
    __tablename__ = "process_log"

    Id = Column(Integer, primary_key=True, index=True)
    Created = Column(DateTime, nullable=True)
    Name = Column(String, nullable=True)
    LogLevel = Column(Integer, nullable=True)
    LogLevelName = Column(String, nullable=True)
    FileId = Column(Integer, nullable=True)
    Args = Column(String, nullable=True)
    Module = Column(String, nullable=True)
    FuncName = Column(String, nullable=True)
    LineNo = Column(String, nullable=True)
    Except = Column(String, nullable=True)
    Process = Column(Integer, nullable=True)
    Thread = Column(String, nullable=True)
    ThreadName = Column(String, nullable=True)

    def __repr__(self):
        return f"ProcessLog('{self.Created}','{self.Name}'," \
               f"'{self.LogLevel}'),'{self.LogLevelName}'," \
               f"'{self.FileId}','{self.Args}','{self.Module}'," \
               f"'{self.FuncName}','{self.LineNo}','{self.Except}'," \
               f"'{self.Process}','{self.Thread}','{self.ThreadName}')"
