#!/usr/bin/env python3

##This script works by you feeding it a file and ensuring that the sha id's is the first element per line in the file.

import cx_Oracle
import getpass

#DB queries to delete the SHA1 references
delete_indexed_archives_entries="delete from indexed_archives_entries where indexed_archives_id in (select indexed_archives_id from indexed_archives where archive_sha1 in ({0}))"
delete_indexed_archives = "delete from indexed_archives where archive_sha1 in ({0})"
delete_node_meta_infos = "delete from node_meta_infos where node_id in (select node_id from nodes where sha1_actual in ({0}))"
delete_node_props = "delete from node_props where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0}))"
delete_stats = "delete from stats where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0}))" #This we had to delete manualy
delete_watches = "delete from watches where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0}))"
delete_nodes = "delete from nodes where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0}))"
delete_binaries = "delete from binaries where sha1 in ({0})"

# #DB queries to select the SHA1 reference, commented out needs some revamp work.
# select_indexed_archives_entries="select * from indexed_archives_entries where indexed_archives_id in (select indexed_archives_id from indexed_archives where archive_sha1 in ({0})) and ROWNUM < 5"
# select_indexed_archives = "select * from indexed_archives where archive_sha1 in ({0}) and ROWNUM < 5"
# select_node_meta_infos = "select * from node_meta_infos where node_id in (select node_id from nodes where sha1_actual in ({0})) and ROWNUM < 5"
# select_node_props = "select * from node_props where node_id in (select node_id from nodes where sha1_actual in ({0})) and ROWNUM < 5"
# select_stats = "select * from stats where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0})) and ROWNUM < 5"
# select_watches = "select * from watches where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0})) and ROWNUM < 5"
# select_nodes = "select * from nodes where node_id in (select node_id from nodes where SHA1_ACTUAL in ({0})) and ROWNUM < 5"
# select_binaries = "select * from binaries where sha1 in ({0}) and ROWNUM < 5"

missing_sha_list = []
#
# #env database connection details
# cx_Oracle_user= input("Enter your username: ")
# #cx_Oracle_pw= input("Enter your password: ")
# cx_Oracle_pw= getpass.getpass("Enter your password: ") #this function hides password output, but will only work in a terminal session
# cx_Oracle_host= input("Enter host with .cisco.com domain: ")
# cx_Oracle_sid= input("Enter Oracle SID: ")
# ox_Oracle_Port= input("Enter a port number: ")


#This function can be used to test a connection to the Oracle DB, Enter the table you would like to run a SELECT query against.
def confirm_connection(connection):
    table_s = input('Enter a table you would like to test query, ie. BINARIES: ')
    cur = connection.cursor()
    cur.execute('select * from {} where ROWNUM < 10'.format(table_s))
    if cur != 0:
        print('Yes we have a connection')
    else:
        print('No, we do not have a connection to DB. Please ensure the database exist')

    cur.close()
    connection.close()

#This function establishes a connection to the Oracle DB
def get_db_connection():
    dsn_tns = cx_Oracle.makedsn(host=cx_Oracle_host, port=ox_Oracle_Port, sid=cx_Oracle_sid)
    connection = cx_Oracle.connect(user=cx_Oracle_user, password=cx_Oracle_pw, dsn=dsn_tns)
    return connection


#This function loops through and takes the first index of each line in the file, converts the string to comma seperated each word and It then assigns the {0} index to the missing_sha_list variable.
def getting_file_list():
    file_path = input('Please enter path to file: ')
    f = open(file_path,'r')
    for sha1 in f:
        s = sha1.split(' ')[0].replace('\n', '')
        missing_sha_list.append(s)
    f.close()


#This function uses the query parameter to run a query agaist oracle DB
def run_select(connection, query):
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    print(result)
    return result


def run_delete(connection, query):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute(query)


    connection.commit()



# #Used to verify that records deleted.
# # Instead of deleteing im doing a batch select, this function, first establishes a connection to the DB and then it ensures that the missing_sha_list is not empty.
# #It then inserts ticks before and after each element in the list and finally runs the query in a specific order.
#commented out needs some revamp work.
# def do_batch_select():
#     connection = get_db_connection()
#
#     if len(missing_sha_list) > 0:
#
#         # if input("Would you like to see the record?  Continue? (y/n): ") != "n":
#         #     print("You will be selecting the following records {}".format(missing_sha_list))
#         if input("Confirm that records have been deleted? Continue? (y/n): ") != "y":
#             exit()
#
#         temp = '\',\''.join(missing_sha_list) #adding tick before and after each object in the list
#         sha_string = f"'{temp}'" #adding tick before and after each object in the list
#
#         a = select_indexed_archives_entries.format(sha_string)
#         b = select_indexed_archives.format(sha_string)
#         c = select_node_meta_infos.format(sha_string)
#         d = select_node_props.format(sha_string)
#         e = select_stats.format(sha_string)
#         f = select_watches.format(sha_string)
#         g = select_nodes.format(sha_string)
#         h = select_binaries.format(sha_string)
#          
#
#
#         print(a)
#         run_select(connection, a)
#
#         print(b)
#         run_select(connection,b)
#
#         print(c)
#         run_select(connection,c)
#
#         print(d)
#         run_select(connection,d)
#
#         print(e)
#         run_select(connection,e)
#
#         print(f)
#         run_select(connection,f)
#
#         print(g)
#         run_select(connection, g)
#         
#         print(g)
#         run_select(connection, g)
#
#     else:
#         print("There is nothing to do, please check ensure there all sha's to delete")
#
#     connection.close()


def do_batch_delete():
    connection = get_db_connection()

    if len(missing_sha_list) > 0:
        if input("Going to delete {} records. Continue? (y/n) ".format(len(missing_sha_list))) != "y":
            exit()
        if input("Would you like to see the records to delete prior to deletion?  Continue? (y/n): ") != "n":
            print("You will be deleting the following records {}".format(missing_sha_list))
        if input("Are you sure you want to delete the records? Continue? (y/n): ") != "y":
            exit()

        temp = '\',\''.join(missing_sha_list)
        sha_string = f"'{temp}'"

        a = delete_indexed_archives_entries.format(sha_string)
        b = delete_indexed_archives.format(sha_string)
        c = delete_node_meta_infos.format(sha_string)
        d = delete_node_props.format(sha_string)
        e = delete_stats.format(sha_string)
        f = delete_watches.format(sha_string)
        g = delete_nodes.format(sha_string)
        h = delete_binaries.format(sha_string)

        print(a)
        run_delete(connection,a)

        print(b)
        run_delete(connection,b)

        print(c)
        run_delete(connection,c)

        print(d)
        run_delete(connection,d)

        print(e)
        run_delete(connection,e)

        print(f)
        run_delete(connection,f)

        print(g)
        run_delete(connection,g)

        print(h)
        run_delete(connection,h)

    else:
        print("There is nothing to do, please check ensure there all sha's to delete")

    connection.close()

def do_dry_run():
    connection = get_db_connection()

    if len(missing_sha_list) > 0:

        if input("Dry-run mode now activated!!, Going to delete {} records. Continue? (y/n) ".format(len(missing_sha_list))) != "y":
            exit()
        if input("Would you like to see the records to delete prior to deletion?  Continue? (y/n): ") != "n":
            print("You will be deleting the following records {}".format(missing_sha_list))
        if input("Are you sure you want to delete the records? Continue? (y/n): ") != "y":
            exit()

        temp = '\',\''.join(missing_sha_list)
        sha_string = f"'{temp}'"

        a = delete_indexed_archives_entries.format(sha_string)
        b = delete_indexed_archives.format(sha_string)
        c = delete_node_meta_infos.format(sha_string)
        d = delete_node_props.format(sha_string)
        e = delete_stats.format(sha_string)
        f = delete_watches.format(sha_string)
        g = delete_nodes.format(sha_string)
        h = delete_binaries.format(sha_string)

        print('The query I will use to delete is..... ' + a)


        print('The query I will use to delete is..... ' + b)


        print('The query I will use to delete is..... ' + c)


        print('The query I will use to delete is.....' + d)


        print('The query I will use to delete is..... ' + e)


        print('The query I will use to delete is..... ' + f)


        print('The query I will use to delete is..... ' + g)

        print('The query I will use to delete is..... ' + h)


        print('Dry-run mode disengaged!!!')


    else:
        print("There is nothing to do, please check ensure there all sha's to delete")

    connection.close()



def main():

    #getting_file_list() #Used to get sha id's from file
    # do_dry_run()        #Used to run a test to see what the delete query will look like without making changes
    # do_batch_delete()   #Used to delete the sha ids
    # # do_batch_select()   #Used to confirm sha's deleted


main()
