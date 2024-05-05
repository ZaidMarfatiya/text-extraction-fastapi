from app.db.session import SessionLocal


def init():
    db_session = SessionLocal()
    db_session.close()

def main():
    init()


if __name__ == '__main__':
    main()
