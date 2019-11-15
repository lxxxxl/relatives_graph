#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


###############################################
# Relative-Parent association mapping
relative_parent_assoc = Table("relative_parent_assoc", 
                            Base.metadata,
                            Column('relative_id', Integer, ForeignKey('relatives.id')),
                            Column('parent_id', Integer, ForeignKey('relatives.id'))
                            )
    


###############################################
# Relative
class Relative(Base):
    __tablename__ = 'relatives'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthdate = Column(DateTime, default=func.now())
    deathdate = Column(DateTime, default=None)
    about = Column(String)
    photo = Column(String)	# TODO check and save as base64
    
    parents = relationship("Relative",
                          secondary=relative_parent_assoc,
			primaryjoin=relative_parent_assoc.c.relative_id==id,
			secondaryjoin=relative_parent_assoc.c.parent_id==id,
			 lazy='dynamic',
                         back_populates="descendants")
    descendants = relationship("Relative",
                          secondary=relative_parent_assoc,
			primaryjoin=relative_parent_assoc.c.parent_id==id,
			secondaryjoin=relative_parent_assoc.c.relative_id==id,
			 lazy='dynamic',
                         back_populates="parents")
    
    def __init__(self, name, birthdate, deathdate, about, photo):
        self.name = name
        self.birthdate = birthdate
        self.deathdate = deathdate
        self.about = about
        self.photo = photo

    def __repr__(self):
    	strBirthdate = "???"
    	if self.birthdate != None:
    		strBirthdate = self.birthdate.strftime('%d.%m.%Y')
    	strDeathdate = "???"
    	if self.deathdate != None:
    		strDeathdate = self.deathdate.strftime('%d.%m.%Y')
        #return "<Relative('%s','%s', '%s', '%s')>" % (self.name, strBirthdate, strDeathdate, self.about)
        return "%s\n%s\n%s\n%s" % (self.name, strBirthdate, strDeathdate, self.about)
    
