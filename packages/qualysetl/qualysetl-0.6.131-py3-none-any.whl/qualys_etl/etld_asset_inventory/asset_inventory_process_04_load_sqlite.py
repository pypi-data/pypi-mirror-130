from qualys_etl.etld_lib import etld_lib_config as etld_lib_config
from qualys_etl.etld_lib import etld_lib_functions as etld_lib_functions
from qualys_etl.etld_lib import etld_lib_sqlite_tables as etld_lib_sqlite_tables

global asset_inventory_sqlite_file


def asset_inventory_sqlite():
    global asset_inventory_sqlite_file

    etld_lib_sqlite_tables.create_table(etld_lib_config.asset_inventory_table_name_software_assetid,
                                        etld_lib_functions.asset_inventory_software_assetid_csv_columns(),
                                        asset_inventory_sqlite_file,
                                        'id_pk', etld_lib_functions.asset_inventory_software_assetid_csv_column_types())
    etld_lib_sqlite_tables.bulk_insert_csv_file(etld_lib_config.asset_inventory_table_name_software_assetid,
                                                etld_lib_config.asset_inventory_csv_software_assetid_file,
                                                etld_lib_functions.asset_inventory_software_assetid_csv_columns(),
                                                asset_inventory_sqlite_file, "software_assetid")

    etld_lib_sqlite_tables.create_table(etld_lib_config.asset_inventory_table_name_software_unique,
                                        etld_lib_functions.asset_inventory_software_unique_csv_columns(),
                                        asset_inventory_sqlite_file,
                                        'fullName')
    etld_lib_sqlite_tables.bulk_insert_csv_file(etld_lib_config.asset_inventory_table_name_software_unique,
                                                etld_lib_config.asset_inventory_csv_software_unique_file,
                                                etld_lib_functions.asset_inventory_software_unique_csv_columns(),
                                                asset_inventory_sqlite_file, "software_unique")

    etld_lib_sqlite_tables.create_table(etld_lib_config.asset_inventory_table_name,
                                        etld_lib_functions.asset_inventory_csv_columns(),
                                        asset_inventory_sqlite_file,
                                        key='assetId')
    etld_lib_sqlite_tables.bulk_insert_csv_file(etld_lib_config.asset_inventory_table_name,
                                                etld_lib_config.asset_inventory_csv_file,
                                                etld_lib_functions.asset_inventory_csv_columns(),
                                                asset_inventory_sqlite_file, "full asset inventory")


def start_msg_asset_inventory_sqlite():
    etld_lib_functions.logger.info(f"start")


def end_msg_asset_inventory_sqlite():
    etld_lib_functions.log_file_info(etld_lib_config.asset_inventory_csv_file, 'in')
    etld_lib_functions.log_file_info(asset_inventory_sqlite_file)
    etld_lib_functions.logger.info(f"end")


def setup_vars():
    global asset_inventory_sqlite_file
    try:
        asset_inventory_sqlite_file
    except:
        asset_inventory_sqlite_file = etld_lib_config.asset_inventory_sqlite_file


def main():
    start_msg_asset_inventory_sqlite()
    setup_vars()
    asset_inventory_sqlite()
    end_msg_asset_inventory_sqlite()


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='asset_inventory_sqlite')
    etld_lib_config.main()
    main()

