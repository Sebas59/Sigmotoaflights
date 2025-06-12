class Vuelo():
    __tablename__ = "Vuelo"
    id_vuelo = Column(Integer, primary_key=True, index=True)
    Origen = Column(String)
    Destino = Column(String)

class usuario():
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    email = Column(String)
   

class Reserva():
    __tablename__ = "Reserva"
    id_reserva = Column(Integer, primary_key=True, index=True)
    id_vuelo
    id_mascota
    



class Mascotas(Base):
    __tablename__ = "Masctota"
    id_mascota = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    id_vuelo = Column(String)
    
    
