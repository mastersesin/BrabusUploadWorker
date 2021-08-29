# NAY XAI TU 15 - 17
import uuid
from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'ty-bucket-farm-1'
RUN_CONFIG = [
    {
        'id': 'drive1',
        'share_drive_id': '0AHc4cl8hf8dPUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM8aqIIMZ7rKjIlDvuZZJCkCLpoUPl4f9Tk6s00UT9KKzPjvvlLcg_nQ3IQfjJ088wL_tFYyp3hgJP71MSBIwdm0gASa3PcWQ6bi7fGx00Jj84uUVHdDCr4hYD-DQttFw2US08ZTz3vPBUQmGkN7RqYg","token_type":"Bearer","refresh_token":"1//0ejRWbAxohOl1CgYIARAAGA4SNwF-L9IrZ9VzQEDlU0VuJpfGWcQsecY8aKoEW5cOZ6Tv5Eq2qNDd5OKGHD3MUp9D5-tYAr5v1wQ","expiry":"2021-08-18T17:21:13.4333271+07:00"}',
            '{"access_token":"ya29.a0ARrdaM_7j2Ck193G3nDHccxAc1j6BtyWd3ncOwyWsiJUIu08NIxv_5Yyl58VHDiICoUeATggG6BJVuH3YtaG7mmVpupZ30pfewdT6dog0N3ERCw8i-qj-HdJKBLgGkJpF2JS5r-cM4BoqdlECeJEdtgK5sDV","token_type":"Bearer","refresh_token":"1//0erabMG6qvP3uCgYIARAAGA4SNwF-L9Ir4AZTAuEDE72oi0C3nZF9xYR0ZnI_wiYcBVIQYYUwUpjuHuJ1h6-_rPP3TUoqye_zyXk","expiry":"2021-08-18T17:21:36.3898538+07:00"}',
            '{"access_token":"ya29.a0ARrdaM99fvNwep80mjSq7E1dsmQ0WLSLOAhvC51LgyMcLlWDl12wV2QemdxQtfA-qqRs0sbq-UjA08bQlQzx_LYVtAL3LXh515h6JzdXfhlCuqFkxYADUxl7Ekp3nD6Om223vxhDKuwWaetI2O6sxlAYbK9D","token_type":"Bearer","refresh_token":"1//0eu-qdyZRbHtLCgYIARAAGA4SNwF-L9IrcaindKOUnc33p0YDLNi_dOrgSbgXkkTPj0sCAGYJD3ZJrPqJFq3apg7UbDWxo4cSeHk","expiry":"2021-08-18T17:22:08.0501874+07:00"}'
        ]
    },

    {
        'id': 'drive2',
        'share_drive_id': '0AObDYgt-8MjpUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM84PAotvR0Q0NF82pZ6H7tvP6RUlwkwNEP2qFsmrsgAvKTc0hURkxOqKQ2UqdqOgI-YsA3gBmi5VOihAJDtT8yxsVyDfLNqtNFZJ0Jn7pCcoWXyaxnTitHuq-795lE-mFoM4ojP_FS_WdgUNsfjXH68","token_type":"Bearer","refresh_token":"1//0esh32Mjf2HHiCgYIARAAGA4SNwF-L9IrHjG9nItmqN0kmi7gFukPOGlMYkyiXfN_caiEAAjCICHOTvpMQ8VTM4LnPPVjkdJgu-M","expiry":"2021-08-18T17:22:26.3790485+07:00"}',
            '{"access_token":"ya29.a0ARrdaM8keoBPBzeTP60FV5z7kZps8lTFpV1JSfqwjVxc4Cj-5I-gbIlZbatI2V9ClYkogqdTjabT6PxJ7aD0fok3AP8wgO1AOjx8HqLh5Xwh62qYuT4I5mG5T7iKTtqTpnIotSkc-rO5rbQgj-63GQ-xaaH2","token_type":"Bearer","refresh_token":"1//0eUfKpsEOlXtACgYIARAAGA4SNwF-L9IrCRygqxeR5jL3KZy2BGw7Clv9ngrWlrxEtq3MiUArw80OcInziIAYAgv5Vujv1JL5S8A","expiry":"2021-08-18T17:23:07.7111659+07:00"}',
            '{"access_token":"ya29.a0ARrdaM8WGJHRCaYyZkc1-pFW1-xs7WIDhd2NZaoIN81CzMjKFiZ-4UcIAwbJEH1OqDnhtLOJX_R7GoCr5RO4IibmSwQV84Z5ps3qv_Apda0685tfYkcT6rdRnQ91xRmfGDUpA0CZDWkVFJfKPHjMU2hMxqtC","token_type":"Bearer","refresh_token":"1//0eeJQGX2PlpH3CgYIARAAGA4SNwF-L9IrRxfDgWIMR4dyl49IIHH2jU0c0Y5_TT5_jK4Qzv9DZCxAX_NLd0jvyVOcvVrTgbvJ6bs","expiry":"2021-08-18T17:23:26.2277692+07:00"}'
        ]
    },

    {
        'id': 'drive3',
        'share_drive_id': '0ABd41mBtM6MZUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM8aGEpNCeZfHogjP6vAHYD-OOOZvpNmSSWKH6u-c5j1nuYVCQ6kGVVhBPlVMaKQ4ku_e321Oj1LZAN4WkLMMwN7FWVnUDnLG9xx7bwhmj4ixAY6d0g8jLN4k2K6KHqWxbDbZ5jEI6ipnYhvvwy3idbT","token_type":"Bearer","refresh_token":"1//0e2FatRlAznF-CgYIARAAGA4SNwF-L9Ir4XdPoyZPPWRHi3uLGsBulI655XVVbhEtnPZfpqCbgra204wMUV6kbB3vcQAZE-SI1-E","expiry":"2021-08-18T17:56:56.8318587+07:00"}',
            '{"access_token":"ya29.a0ARrdaM-2kd09_0533BTxgDDIriNd4fVQ2vO1uGs35GjF3azNx4KOZiD9AutrIQ_uNL8ZLhgSZsz025w5KPfrkc7SdiF_ELM9PJ1VARb7K4-kNH0OvKG6wAn0k9b5xoC1g8ZTyLT3Q1UH-lYPS9vVYPfb0_Zq","token_type":"Bearer","refresh_token":"1//0edsTopwc4QTACgYIARAAGA4SNwF-L9Ir5vJVKbMBZEXGjCUrPiHXi1_Yj1PJ23NibqgwVp4OSu8NaVrR18U1TfqtKWPnoO1K_so","expiry":"2021-08-18T17:57:15.2236298+07:00"}',
            '{"access_token":"ya29.a0ARrdaM8N3MY4gNFF7e5ZArwitg001n9PDGskpsQ_mPz5FTx32U1wpSQs_J3Q9qEQGIFsq0ZsBxCIC1IfTU51B2ELC0036hdxiitrNmSMX0C1uuKKX4TMTWRKrFNZOjAh4MeAEsPazndfkA8IWtZ17CcNE1qy","token_type":"Bearer","refresh_token":"1//0eXrq1QFoSd-WCgYIARAAGA4SNwF-L9IrMsJTIvSkg3cLGXnWKLVj463sryfZ68Vynjisp9HoSqFthZhEoAqXjasgdl8PQaDPugw","expiry":"2021-08-18T17:57:34.3791653+07:00"}'
        ]
    },

    {
        'id': 'drive4',
        'share_drive_id': '0ANn4jQv0I66MUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM_qNyN6KfOfRh21pzdOWSgaICYXewuugiNUt0P_xYxx-ETXBOjpb99H2OAAsn6TQMEEBaslgyHI3LFl5V_QoG1fVsEe3gHGiPehknO3MXBhmpXGpWGTctZHV3eLQRw-GzJBvqIMlvUwNW4VYhbd6c77","token_type":"Bearer","refresh_token":"1//0em5ScwfPRXdxCgYIARAAGA4SNwF-L9Ir5FfPiURD6eec1hs9rsEfA5xPhNYM10y0yEvQSvziGM6jb2XFDva0yHl6U0PtyCUsi3E","expiry":"2021-08-18T17:57:52.9130138+07:00"}',
            '{"access_token":"ya29.a0ARrdaM_UcyUK79hZrzzxaEx3lQSx8vTlxIXOiiTYlXhcb9b138b-I_naUxP9aeTHTtgzaM1_HkQILNlwIyKHrkjJO0SLtHz5Oa4hJp-KUm7dfteKXNk1cxHFTWw_xGxC2g3_iJ7q9bPmUlNviJ3Kvthp1DrI","token_type":"Bearer","refresh_token":"1//0eK-OaoKoMk8HCgYIARAAGA4SNwF-L9IrYg1jREs2A0svmWtDnrkLYtac_IhY-VV7x8RVeSUvR_jRw22riYYymlyyNE-CRBNzFKs","expiry":"2021-08-18T17:58:12.325797+07:00"}',
            '{"access_token":"ya29.a0ARrdaM-1iC4f01NIQoZDHJeKiRL3fU486au-XTeD2v9TTvMOPb4b75JaZyO2s4GNdZdQy2OfQmxOu2Q1vYBDXlBGBSS0BZIu1x8BwqQcIM7DUIfdh40gmymQAjeHOUyAzwDtMCujWdGJ6ljYQGLWNxD8RNeG","token_type":"Bearer","refresh_token":"1//0eqB-OEuq2KkxCgYIARAAGA4SNwF-L9IroJov-avKSLou-A4hOfrwIbFt05HaOFBJxorIr7pGRYA209EoWYR9LKLfleg1exctMUo","expiry":"2021-08-18T17:58:51.1117722+07:00"}'
        ]
    },

    {
        'id': 'drive5',
        'share_drive_id': '0AN6xunQhSVpJUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM87tYyrsbxelZ94XD8nhm0xiDqQZN8xftJJ3f0OsffzODiMdR9ZJsuts6UgowFhh1mldLwQ3RF0TMVeIuhZIMGaef3D-k6oxwoZWWPmmyLJlrhxwdxh_kLaYpGVgaG3wxWODmpYuXdc3fAf9iLObI-h","token_type":"Bearer","refresh_token":"1//0ejyaJWyzJS5XCgYIARAAGA4SNwF-L9IrRt5sh3glYPkEwgRu6e_iUJXEXh2Gp1NJtgwvfR_AP0Ids0A0e5SkLvo8OtxRgd36GwM","expiry":"2021-08-18T17:59:10.1335999+07:00"}',
            '{"access_token":"ya29.a0ARrdaM85TGhx5MdhmHTaiySWB5rwgohNJeuLkpdq3YTBE97h_ga6AijJzbBi66AntYC8UeNCOQarWbLOJJLcZMffbSzdl10-EbUazC3t_vWtu6boIK1LZmXyqjm4exnnJF6bCSRYs7uzSEityJyz3nBbdsrY","token_type":"Bearer","refresh_token":"1//0eCRrGrMf-8nPCgYIARAAGA4SNwF-L9Irvj6DEnJUI0zQhhF4LMNEb0AeX_FAt-xnDJjHiM1waW3YdluIBc11gHpj6emEmQ1ibn8","expiry":"2021-08-18T17:59:28.9706329+07:00"}',
            '{"access_token":"ya29.a0ARrdaM87XxrJrz7_ojW34LR6aW8aXWhklnwALz-Y1cZEboUKvWOrPtxKJW6uh5IPHW5EXSd_JVxcJEqLV744Qi-VFsnmURHoXor8m_0lKNu1XkIj-UE11-QkxD_VNnG4NxXRznna-QXweQbfCu_1TMu5QsfQ","token_type":"Bearer","refresh_token":"1//0erxTF2vWEm5uCgYIARAAGA4SNwF-L9IrGzPFGRq1PwtzpIa5Pdrgb390oPMpufgCKmqbneHBPJR5OAzAa3a1DxNR9NL6ndUw28g","expiry":"2021-08-18T17:59:54.3118044+07:00"}'
        ]
    },

    {
        'id': 'drive6',
        'share_drive_id': '0AO_0DQeT7ontUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM_vJqgIhh0USGARXKL-82nuMTxn8Y50iq-KxrzbsTdBGnGoGOhwyT97YXXUWXGFt6wyiXOVc0hlk20VwRngrbKCwmjuEZsledIUfLPU_eI96PnVcZ-shjxcj-CYCGM4zAp-KCza_3-6c5ecfWIWKw1l","token_type":"Bearer","refresh_token":"1//0es-blbjS1cUjCgYIARAAGA4SNwF-L9IrF8z5T3YmbhnB91QQljCRmU7jEgaX4xYMZ8Tp2lwYb44IW7dsYFucDXF3S7t8jo8ST_0","expiry":"2021-08-18T18:00:13.3013895+07:00"}',
            '{"access_token":"ya29.a0ARrdaM9bo7CfFWEKwor2amK-SJLb7S5n5TpNbAC_w56x-xpBaxr19f9r8fyka3Ae0_aKlCgakh0S7-VhM2Jufz5NtHQc4s0ok61kbVACLblGdc1TzzMO01DSRhAHDaZlLenWQa-0HfoVmXkxdHKMdMU6je9O","token_type":"Bearer","refresh_token":"1//0eF68Vfsh-UkfCgYIARAAGA4SNwF-L9Iru_M2torazBh13a49Gbcta4vlV3wE0pvJHtGURt31aM7_dZEMjWF9MYjFy1WD6IUN9HI","expiry":"2021-08-18T18:00:32.1397908+07:00"}',
            '{"access_token":"ya29.a0ARrdaM_22OprNPEAbsxe2cGBQtzWqNwdrvveoNGTRQQMsT3TlxPJ-MKZMRMwBKjSiXQxfx1sTcr4sbPW5GtOtxT0BbUUoETXyG3-_bqWvciRaYFIWPeHHnhP8AY_281G3SMIVJiTTmi6M55r78Gz-r-dTMAO","token_type":"Bearer","refresh_token":"1//0e0P5bJGtrvnwCgYIARAAGA4SNwF-L9IrCuYyZaKKeMTnXNLvSO-rrFRVAoamThEKZ796rZGpvUjU8qifmL8POAg4SJHQgSBTXnM","expiry":"2021-08-18T18:00:51.8799223+07:00"}'
        ]
    },

    {
        'id': 'drive7',
        'share_drive_id': '0ALKCQW5S-mpzUk9PVA',
        'list_rclone_token': [
            '{"access_token":"ya29.a0ARrdaM_XfcpNNkpkemjwN4BxsUYx0QN5BLOq3OYZD6hzmngVvWEkU113_gMFyAyERbtI84z4PL-Tky0qFbkgOyoGa8UffIbmg3toqUkcuSKHCKSzbdAB6ILYCy_ZiVe15VKabJTsYwLBf6RGuU2oWHb_cRv8","token_type":"Bearer","refresh_token":"1//0eUvHcqM39IQMCgYIARAAGA4SNwF-L9Ir9zMxSp7mMPnfRNr_DP01nE9j9hxdGIR33Cw9RO5lSNR3674On2CiEHyqOBEqiZ5BmSk","expiry":"2021-08-18T18:01:19.271579+07:00"}',
            '{"access_token":"ya29.a0ARrdaM9ZoAswoFWsRBLmR46XSqkcpdFwqrtzCXYWryPjbJoUI_R5hy_5M7HAqXCNuY106IHNda_qOYgCtAVZoaIcwJTQq5nhGrssLzpIB02Wp_hK5EJ4ElCdMFjaOoSMAWNyLUIGRFvxLtyyGBuer9KltjnB","token_type":"Bearer","refresh_token":"1//0e6BhtL9tjaCdCgYIARAAGA4SNwF-L9Ir6wHJQiT6PNZXMl2I7OH51XWQ4agPTA37kZMO3VwOJheqZ0o6UmKy9CEkzc2jNJU2hdI","expiry":"2021-08-18T18:01:40.4637161+07:00"}',
            '{"access_token":"ya29.a0ARrdaM-A1jUkQxa4RETDXQ3juiTP2DiV8tMbx8KEO8XL0x2wOu9Fus4o8Ts4Un1FBx1REn2EGQn6ZjqaAMyTRFTCI7lnmh07-VqnmHMdFuYIDT7phZHzxtAxbIzH8x-L47vdqY7U001d2M-EaTPJV4kCVoO1","token_type":"Bearer","refresh_token":"1//0evz2fGo-imWwCgYIARAAGA4SNwF-L9IrcrAGGq8augINLBm3tx-k0HwmpXPs7Cg1ZNX7c017IALrPFfTyWc66uXmHwTElGgeUj8","expiry":"2021-08-18T18:02:02.1881709+07:00"}'
        ]
    }

]
PROCESS_COUNT = 16

RCLONE_TEMPLATE = """
[{mount_name}]
type = drive
scope = drive
token = {token} 
team_drive = {drive_id}
root_folder_id =
"""
RCLONE_CONFIG_ABS_PATH = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]


def process(abs_file_path):
    os.system('python3 upload_to_gcs.py {} {}'.format(abs_file_path, BUCKET_NAME))


def mount_drive_disk(rclone_mount_name, token, drive_id):
    os.system("echo '{}' >> {}".format(RCLONE_TEMPLATE.format(
        mount_name=rclone_mount_name,
        token=token,
        drive_id=drive_id
    ), RCLONE_CONFIG_ABS_PATH))
    cm = os.system('mkdir {}'.format(rclone_mount_name))
    if cm != 0:
        os.system('fusermount -u {}'.format(rclone_mount_name))
    os.system(
        'rclone mount {}: {} --vfs-read-chunk-size 256M --transfers 16 &'.format(rclone_mount_name,
                                                                                 rclone_mount_name, ))


if __name__ == "__main__":
    processes = []
    for config in RUN_CONFIG:
        share_drive_id = config.get('share_drive_id')
        list_rclone_token = config.get('list_rclone_token')
        mount_id = config.get('id')
        for rclone_token_index in range(len(list_rclone_token)):
            mount_drive_disk(mount_id, list_rclone_token[rclone_token_index], share_drive_id)
            current_process_path = os.path.join(CURRENT_EXEC_PATH, mount_id)
            while len(os.listdir(current_process_path)) == 0:
                print('List dir not updated yet wait 1 sec')
                time.sleep(1)
                continue
            if os.path.exists(current_process_path):
                folder = os.listdir(current_process_path)[rclone_token_index]
                print('Current process {}'.format(folder))
                for file in os.listdir(os.path.join(current_process_path, folder)):
                    if file.endswith('.csv'):
                        p = Process(target=process, args=(os.path.join(current_process_path, folder, file),))
                        processes.append(p)
                        p.start()
                    while len(processes) >= PROCESS_COUNT:
                        processes = [running_process for running_process in processes if running_process.is_alive()]
                        time.sleep(0.01)
                for p in processes:
                    p.join()

            else:
                print('{} not existed'.format(current_process_path))

# for file in os.listdir():
#     if os.path.isdir(file):
#         print(file)
#         os.system('chia plots add -d /home/ty/cloud3bucket2/{}'.format(file))
