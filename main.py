import csv
from sqlalchemy import create_engine, String, Integer, Boolean, MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session

engine = create_engine("postgresql+psycopg2://ewan:secret@127.0.0.1:5432", echo=True)


class Base(DeclarativeBase):
    pass

class Passenger(Base):
    __tablename__ = 'passenger'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String(20))
    cabin: Mapped[str] = mapped_column(String(20))
    survived: Mapped[bool] = mapped_column(Boolean)
    def __repr__(self):
        return f"id={self.id}  name={self.name} age={self.age} sex={self.sex} cabin={self.cabin} survived={self.survived}"


with open('./titanic.csv', newline='') as datafile:
    with Session(engine) as session:
        datareader = csv.DictReader(datafile)
    for row in datareader:
        # print(row['PassengerId'], row['Name'], row['Age'], row['Sex'], row['Cabin'], row['Survived'])
        def surv(data:str):
            if data == '1':
                survived = True
            else:
                survived = False
            return survived
        def ages(data:str):
            if data == '':
                ages = 0
            else:
                ages = int(float(data))
            return ages
        newPassenger = Passenger(
            name=row['Name'],
            age=int(ages(row['Age'])),
            sex=row['Sex'],
            cabin=row['Cabin'],
            survived=surv(row['Survived'])
        )
        session.add(newPassenger)
        session.commit()

if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)
    print("Created Database !")

#  docker run --name titanic_db -e POSTGRES_USER=ewan -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:latest
