from sqlalchemy import create_engine, select,and_,func,update,delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine=create_engine('sqlite:///data.db')

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

class Account(Base):
    __tablename__="account"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column()
    balance:Mapped[int]=mapped_column()

Base.metadata.create_all(engine)

# with Session(engine) as session:
#     user1=User(name="name1")
#     session.add(user1)
#     session.commit()
#     print("user1 saved")
#     print("Product ID:", user1.id)

with Session(engine) as session:

    # user1=User(name="name2")
    # user2=User(name="name3")
    # user3=User(name="name4")
    # session.add(user1)
    # session.add(user2)
    # session.add(user3)
    # session.commit()
    

    # # multiple data in one go
    # # prepare the query
    # query=select(User)
    # # execute the query and get all the result
    # users=session.scalars(query).all()

    # # users is the iterator we can iterate by for loop and get the result
    # for user in users:
    #     print(user.id,user.name)


    # # to fetch only single data with where clause
    # query = select(User).where(User.id == 2)

    # user1=session.scalars(query).first()
    # print(user1.id,user1.name)

    # # orderby clause
    # print("order by clause----------------")
    # query=select(User).order_by(User.id.desc())
    # data=session.scalars(query)
    # for i in data:
    #     print(i.id,i.name)

    # # limit 
    # print("limit usage in orm-------------------")
    # query=select(User).order_by(User.id.desc()).limit(1)
    # data=session.scalars(query).all()
    # for i in data:
    #     print(i.id,i.name)

    # # Update the row
    # print("update the row")
    # user=session.get(User,1)
    # if user:
    #     user.name="anmol"
    #     session.commit()
    #     print("user name updated")

    # # delete the record
    # # print("delete the records")
    # # user=session.get(User,2)
    # # if user:
    # #     session.delete(user)
    # #     session.commit()
    # #     print("user deleted")


    # # To select the things from to do some operation
    # # .get() is use to fetch by primary key
    # print(" usage of .get()")
    # user = session.get(User, 1)
    # if user:
    #     print(user.name)

    
    # #  .scalars() is use to select the model object 
    # print("usage of scalar")
    # all_user=session.scalars(select(User)).all()
    # for u in all_user:
    #     print(u.id,u.name)

    # # .execute() usage to execute the queries
    # users=session.execute(select(User.name)).all()
    # for i in users:
    #     print(i.name)

    # stmt=User(name="name1")
    # session.add(stmt)
    # session.commit()

    # # where clause
    # stmt=select(User).where(User.name=="name1")
    # users=session.execute(stmt).scalars().all()

    # for i in users:
    #     print(i.id)

    # #  where and condtion with and operator 
    # stmt=select(User).where(
    #     and_(
    #         User.name=="anmol",
    #         User.id==1
    #     )
    # )
    # result=session.execute(stmt).scalars().all()
    # for i in result:
    #     print(i.id,i.name)

    # # where condition in in_ 
    # stmt=select(User).where(
    #     User.name.in_(
    #         ["name1","name3"]
    #     )
    # )
    # result=session.execute(stmt).scalars().all()
    # for i in result:
    #     print(i.name)
    # print("order by -----------------")
    # stmt=select(User).order_by(func.lower((User.name)))
    # result=session.execute(stmt).scalars().all()
    # for i in result:
    #     print(i.id,i.name)

    # print("this is to update----------")
    # # stmt=update(User).where(User.id==1).values(name="Anmol Prakash")
    # # result=session.execute(stmt)
    # # print(result.rowcount)
    # # session.commit()

    print("this is to delete the rows")
    # stmt=delete(User).where(User.id==2)
    # result = session.execute(stmt)
    # print(result.rowcount)
    # session.commit()


# with Session(engine) as session:
    # accounts = [
    #     Account(name="name1", balance=10000),
    #     Account(name="Aman", balance=15000),
    #     Account(name="Rahul", balance=20000),
    #     ]

    # session.add_all(accounts)
    # session.commit()
    

print("transactions------------")
# transaction is the group of database operation which can be commited once
# session have feature of rollback the transation transcation completed commit 
# roleback is used in try except block if we are not using the begin
# roleback is only removes uncommited changes

with Session(engine) as session:
    with session.begin():
            stmt=update(Account).where(Account.id==2).values(balance=Account.balance+200)
            session.execute(stmt)
            
            # raise ValueError("Something went wrong")

            stmt=update(Account).where(Account.id==2).values(balance=Account.balance-100)
            session.execute(stmt)
