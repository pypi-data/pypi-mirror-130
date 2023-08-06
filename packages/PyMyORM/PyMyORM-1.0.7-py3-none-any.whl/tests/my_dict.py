from pymyorm.database import Database
from config import db
from models.user import User


def main():
    Database().debug(debug=True)
    Database().connect(**db)

    # case 1
    one = User.find().where(name='ping').one()
    for k in one.keys():
        print(one[k])
    # print(dict(one))

    # case 2
    all = User.find().select('name').all()
    tmp = [dict(one) for one in all]
    print(tmp)


if __name__ == '__main__':
    main()
