# -*- coding: utf8 -*-
import sqlite3


def main():
    global con, cur

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()


async def add_user(telegram_id, full_name, blocked, data_registration):
    main()
    cur.execute(
        f"INSERT INTO Registration (telegram_id, full_name, blocked, data_registration) "
        f"VALUES('{telegram_id}', '{full_name}', '{blocked}', '{data_registration}')")
    con.commit()
    con.close()


async def update_balance(telegram_id, balance, profit, trans):
    main()
    cur.execute(
        f"UPDATE PersonalAccount SET trans='{trans}', balance='{balance}', profit='{profit}'"
        f" WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def update_rev_balance(telegram_id, balance, RevshareBalance):
    main()
    cur.execute(
        f"UPDATE PersonalAccount SET  balance='{balance}', RevshareBalance='{RevshareBalance}'"
        f" WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def add_lk(telegram_id, link):
    main()
    cur.execute(
        f"INSERT INTO PersonalAccount (telegram_id, balance, trans, link, profit, RevshareBalance) "
        f"VALUES('{telegram_id}', '0', '0', '{link}', '0', '0')")
    con.commit()
    con.close()


async def add_ct(telegram_id):
    main()
    cur.execute(
        f"INSERT INTO CT (telegram_id, count) VALUES('{telegram_id}', '0')")
    con.commit()
    con.close()


async def get_ct(telegram_id):
    main()
    cur.execute(
        f"SELECT * FROM CT WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def update_ct(telegram_id, count):
    main()
    cur.execute(
        f"UPDATE CT SET count='{count}' WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def add_stop(telegram_id, stop):
    main()
    cur.execute(
        f"INSERT INTO StopTransaction (telegram_id, stop) VALUES('{telegram_id}', '{stop}')")
    con.commit()
    con.close()


async def add_trans(telegram_id, balance, profit, end_time, state):
    main()
    cur.execute(
        f"INSERT INTO Transact (telegram_id, balance, profit, end_time, state) "
        f"VALUES('{telegram_id}', '{balance}', '{profit}', '{end_time}', '{state}')")
    con.commit()
    con.close()


async def add_rev(telegram_id, rev_id):
    main()
    cur.execute(
        f"INSERT INTO RevShare (telegram_id, rev_id) "
        f"VALUES('{telegram_id}', '{rev_id}')")
    con.commit()
    con.close()


async def add_summ(telegram_id, status, summ):
    main()
    cur.execute(
        f"INSERT INTO payment (telegram_id, status, summ) "
        f"VALUES('{telegram_id}', '{status}', '{summ}')")
    con.commit()
    con.close()


async def get_payment(telegram_id):
    main()
    cur.execute(f"SELECT * FROM payment WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_all_users():
    main()
    cur.execute(f"SELECT * FROM Registration WHERE blocked=False")
    rows = cur.fetchall()
    con.close()
    return rows


async def delete_trans(telegram_id):
    main()
    cur.execute(
        f"DELETE FROM Transact WHERE telegram_id = '{telegram_id}'")
    con.commit()
    con.close()


async def delete_ct(telegram_id):
    main()
    cur.execute(
        f"DELETE FROM CT WHERE telegram_id = '{telegram_id}'")
    con.commit()
    con.close()


async def delete_get(telegram_id):
    main()
    cur.execute(
        f"DELETE FROM GetMoney WHERE telegram_id = '{telegram_id}'")
    con.commit()
    con.close()


async def select_all_getmoney():
    main()
    cur.execute(f"SELECT * FROM GetMoney ")
    rows = cur.fetchall()
    con.close()
    return rows


async def add_get_money(telegram_id, end_time):
    main()
    cur.execute(
        f"INSERT INTO GetMoney (telegram_id, time_end) "
        f"VALUES('{telegram_id}', '{end_time}')")
    con.commit()
    con.close()


async def update_only_balance(telegram_id, balance):
    main()
    cur.execute(
        f"UPDATE PersonalAccount SET balance='{balance}' WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def get_trans(telegram_id):
    main()
    cur.execute(
        f"SELECT * FROM Transact WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def get_all_payment():
    main()
    cur.execute(
        f"SELECT * FROM payment ")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_all_trans():
    main()
    cur.execute(f"SELECT * FROM Transact ")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_all_stop(telegram_id):
    main()
    cur.execute(f"SELECT * FROM StopTransaction WHERE telegram_id = '{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def delete_stop(telegram_id):
    main()
    cur.execute(
        f"DELETE FROM StopTransaction WHERE telegram_id = '{telegram_id}'")
    con.commit()
    con.close()


async def delete_payment(telegram_id):
    main()
    cur.execute(
        f"DELETE FROM payment WHERE telegram_id = '{telegram_id}'")
    con.commit()
    con.close()


async def select_all_rev(telegram_id):
    main()
    cur.execute(f"SELECT * FROM RevShare WHERE rev_id = '{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def subscriber_exists(telegram_id):
    main()
    cur.execute(f"SELECT * FROM Registration WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def get_lk(telegram_id):
    main()
    cur.execute(f"SELECT * FROM PersonalAccount WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def count_users():
    main()
    cur.execute(f"SELECT COUNT(*) FROM Registration WHERE blocked=False")
    rows = cur.fetchall()
    con.close()
    return rows
