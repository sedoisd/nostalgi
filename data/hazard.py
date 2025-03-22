import sqlalchemy
from .db_session import SqlAlchemyBase



class Hazard(SqlAlchemyBase):
    __tablename__ = 'hazards'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

association_table = sqlalchemy.Table(
    'job_to_hazard',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('job', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('hazard', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('hazards.id'))
)
