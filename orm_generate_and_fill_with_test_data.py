#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_defs import Base, Relative

import random


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

session = scoped_session(sessionmaker(bind=engine))


relative1 = Relative("Relative 1",datetime.now(),datetime.now(),"about1","photo1")
session.add(relative1)

relative2 = Relative("Relative 2",datetime.now(),datetime.now(),"about2","photo2")
session.add(relative2)

relative3 = Relative("Relative 3",datetime.now(),datetime.now(),"about3","photo3")
session.add(relative3)
relative3.parents.append(relative2)

for i in range(5):
	r = Relative("subrelative "+str(i),datetime.now(),datetime.now(),"about"+str(i),"photo"+str(i))
	session.add(r)
	r.parents.append(relative3)
	
	r2 = list(range(3))
	random.shuffle(r2)
	for e in r2:
		r3 = Relative("subsubrelative "+str(i)+" "+str(e),datetime.now(),datetime.now(),"about"+str(e),"photo"+str(e))
		session.add(r3)
		r3.parents.append(r)
	
	

relative4 = Relative("Reltative 4",datetime.now(),datetime.now(),"about4","photo4")
session.add(relative4)

relative5 = Relative("Relative 5",datetime.now(),datetime.now(),"about4","photo5")
session.add(relative5)
for i in range(5):
	r = Relative("subr5 "+str(i),datetime.now(),datetime.now(),"about"+str(i),"photo"+str(i))
	session.add(r)
	r.parents.append(relative5)
	
	r2 = list(range(3))
	random.shuffle(r2)
	for e in r2:
		r3 = Relative("sub_new "+str(i)+" "+str(e),datetime.now(),datetime.now(),"about"+str(e),"photo"+str(e))
		session.add(r3)
		r3.parents.append(r)
		


relative1.parents.append(relative2)
relative1.parents.append(relative4)




session.commit()
