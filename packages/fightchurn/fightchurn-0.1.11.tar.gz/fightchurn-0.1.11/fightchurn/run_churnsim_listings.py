import fightchurn.run_churn_listing
from fightchurn.datagen import churndb
from fightchurn.datagen import churnsim
from fightchurn.datetime import date


def run_all(db, user,password,output_dir='../../../fight-churn-output/',init_customers=500,schema='socialnet7'):

    run_churn_listing.set_churn_environment(db, user,password,output_dir)

    churndb.setup_churn_db(schema)

    start_date = date(2020, 1, 1)
    end_date = date(2020, 6, 1)
    churnsim.run_churn_simulation(schema, start_date=start_date, end_date=end_date,
                                                     init_customers=init_customers)

    # churn rate
    for list_num in range(1,6):
        run_churn_listing.run_listing(2, list_num, schema=schema)

    # simple counts
    for list_num in range(1,3):
        run_churn_listing.run_listing(3, list_num, schema=schema)

    # event QA
    run_churn_listing.run_listing(3, 11, schema=schema)
    for vers_num in range(1,9):
        run_churn_listing.run_listing(3, 9, version=vers_num, schema=schema)
        run_churn_listing.run_listing(3, 10, version=vers_num, schema=schema)

    # standard metric names
    for vers_num in range(1,12):
        run_churn_listing.run_listing(3, 4, version=vers_num, schema=schema)

    # Account tenure metric
    run_churn_listing.run_listing(3, 13, schema=schema)

    # standard metrics
    for vers_num in range(1,9):
        run_churn_listing.run_listing(3, 3, version=vers_num, schema=schema)
        # metric QA
        run_churn_listing.run_listing(3, 6, version=vers_num, schema=schema)
        run_churn_listing.run_listing(3, 7, version=vers_num, schema=schema)

    # Metric coverage
    run_churn_listing.run_listing(3, 8, schema=schema)

