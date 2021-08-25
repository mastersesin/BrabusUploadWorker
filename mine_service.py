# # HNAY xai 1 - 14
# import json
# drive_list = [
#     '0AJlOCO3IjHM_Uk9PVA',
#     '0AN_TOTL83hyDUk9PVA',
#     '0AK0q1Uag3cwRUk9PVA',
#     '0AJDtaOmOdPQTUk9PVA',
#     '0AEHdnWLtSRFBUk9PVA',
#     '0AAS-uinMbL61Uk9PVA',
#     '0ALVnDA8bSdc_Uk9PVA',
#     '0ANDhH3MC4qetUk9PVA',
#     '0ACl1JQNXQJqfUk9PVA',
#     '0AO6TImdpqbw-Uk9PVA',
#     '0AE1iP6a_uDIHUk9PVA',
#     '0AHYExRTv9-FcUk9PVA',
#     '0ADwyO48NMBL8Uk9PVA',
#     '0AEM32z9-x-HeUk9PVA'
# ]
# token_list = [
#     {
#         "access_token": "ya29.a0ARrdaM8lJwNxpRBJHK6CgnrugokxNJznbDuh9oIzpsqaTShUSPRcXIbrnWYz9EP8ja3GkGkjf-M-gp35YoMDuAGuSq5nD9Tx3AaNqAPMTHHy0pewARtx8oKjJ6LpU0kViL6CDSwNjVVHO7mmU9qGvS5XLFjJ",
#         "token_type": "Bearer",
#         "refresh_token": "1//0e9_24xHw3rBICgYIARAAGA4SNwF-L9Irx3AxzBHaCQGz1hq55jHMZFB0SPGUPi4l2b3-82Gix2SviuiQ5TcmIWTBH3k57y3ZJvI",
#         "expiry": "2021-08-14T12:37:22.9169448+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM_4TJXY8Vq473NX7eeNEYjy8ZzhYpwaYK7T91JcU4v2hOnfTcpFsL-5y45FGzObzR1t1quT8KUQcQQEGwd8B0aoeiv4Tl4t2ivnMeXUuiAc-NayZzIfdJk952kOQhpChb9jy2iWkt-1G_RDd-OvOPF7",
#         "token_type": "Bearer",
#         "refresh_token": "1//0emaXFJRLdL44CgYIARAAGA4SNwF-L9IrkxOzU4UpNItmTPbgZYMniJEDX4GbPaMniN5fdSVui17S_t4d8YS9tfuVFdyjKp42jRg",
#         "expiry": "2021-08-14T12:38:05.4031853+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM8Lz404YIwGfQA0AZyRDyiUEdl1EnsSVyJU9nzf2pqjp1hpLCvdGwvJxV8dl7xoznSiArxeQgsfS0EwMUOZbj4nvCi35tyY20t-aquu3JWVlB9RRC2lGxdyrlh6bygFBwjQpOMh2wuzX9NVAd4ugV7o",
#         "token_type": "Bearer",
#         "refresh_token": "1//0equWM4Fn05k2CgYIARAAGA4SNwF-L9IrOsctPVFtTqjpoVd0IBgL8-7AJsAkLJJ-53z0jDPEbHzowMmbpSi_d2bVWqAYdpgy5cQ",
#         "expiry": "2021-08-14T12:38:41.4344912+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM8UxnqaN2yCMTD4Ew357GcLAg1QxnR2o1-YjstITHwh74-nKuoVJoNK_c3vH4bXZ7NFJhQj7DoTtRkomHDuSitqzziX-fKUrgPllUgtSb44wFx7MDRjC_kD_WCGiQTyV9Z-Q4GFmeDUUTPz2RWKSmIy",
#         "token_type": "Bearer",
#         "refresh_token": "1//0eHUeOjpr1SqDCgYIARAAGA4SNwF-L9IrYYe_-C9xOR9JCym7oSu9XUXcWUcaaXtL-rxI2IUingtNuPwsJUZCUaQkO0k4Taty-Cw",
#         "expiry": "2021-08-14T12:40:13.1411922+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM_aZPHYWTctq9CwusklReIwV7iDY1bJjOwv8KShhZmXD7Cbvh8lN9PdAx1_3hCqXSKWxa7IhbZqBS2WyNaACXOIq_vsFG48fee23pomdc7dCz-rKPXn1YIpwrnPLcXFJDBOTWOsBgSA1now9tJwsvO5",
#         "token_type": "Bearer",
#         "refresh_token": "1//0ebQDPjlxeDxzCgYIARAAGA4SNwF-L9IrAJhOkkPHP8c9G0I4xBWNUwVJnRJB7CPCjvbwspEUC9SQbQ-jMJV2b9SKiOaklT44ZVg",
#         "expiry": "2021-08-14T12:40:38.8967961+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM9aOY7K0b4LCJOuOszULKQX9DQ_sqzFrndHvX6sdtbuiixLELkBgIS-6fEUFyRC2CFHoAPOqkcV9jKW_kQHBe71MYJ48GMv5aJZzzTKU-Lx1Tix7XL-3y3RHzL5jsco61O9vmMJp_AhYf4OuLRPZVS5",
#         "token_type": "Bearer",
#         "refresh_token": "1//0e9lvSYzpbc0YCgYIARAAGA4SNwF-L9IrDS4XMu3E8677gNb8IYB6xLBEdIg_uMI49hF_EJ2Nv-rpVgSAYD7nZPD72QHQTwAPe20",
#         "expiry": "2021-08-14T12:41:09.0190444+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM9TioL2Asepwz4BKxg9ZWQW9Y4Q68cLi4XNNFmnwvaoV7mQg8A8ddhghKKLVU4TtmG3HNMrl7WpwPCgBMJXFOMDmh5XGhF2u64CiFOOSQ5EnO-6LcAgsg4qY8mbnWxt6ZyyRGP5lGuvVGRkV-apLD4_",
#         "token_type": "Bearer",
#         "refresh_token": "1//0emgy_LYm5cI5CgYIARAAGA4SNwF-L9IrT0Q6I0jl2OBsOkgBkaaaf3b8W2f1h8_cE3e0lS9JSo6OgrW6FsVl8MxibBXn1-KVuyQ",
#         "expiry": "2021-08-14T12:41:36.3647921+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM8cRtUx9RabsmZo12tyZ9ILBYWAmDbwwzsXTIVTVXU_7aA1db_nEmrsaGvdWqJuJBLEj-Je5CidGWE7qCoxykjzjaZOnmlERZf3FIYgDWK2fNoEKJigrbnFfiHc4U3dgmVgQfca2HlFl2uig5eMCU-J",
#         "token_type": "Bearer",
#         "refresh_token": "1//0eTioqEUVVBncCgYIARAAGA4SNwF-L9IrElu4-ZoMkq9zVKOVsBt_70umbLtkB46jBBzuzBJYoBd15vxd6QA8x6gbopfaSeg3k_E",
#         "expiry": "2021-08-14T12:42:06.245164+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM8vemKm9FT5bYpuCfiwpul9ZrG4NjjhJXPN-M5jPMmXBxmyLYZXl71UHY2XBHkeHhwb7ldhSeqoxjcWUMxBeJnDcK0SFL46JJuoza-g82hhbTMig-To_7_1mMPRD234I2jOvmcJ5RcloO4Hpl7lxJ7B",
#         "token_type": "Bearer",
#         "refresh_token": "1//0eEi2aV6o_n2DCgYIARAAGA4SNwF-L9IrXA6wAFYibtbGny_xH_dqzjxotwR0eE8CA1Nc9UXI0nhaT2ybfdRlpOdKpSJiiDLRW14",
#         "expiry": "2021-08-14T12:42:39.0119053+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM-Ub5J_BEuEZNo_txX1IL3_cKvSx8hTf8Zo8xBJ5MCyQHOhULriMJNp26V9x3nR00Nm-yBIf-PxynbvXbkjum_fg84zPTHPkKyb7-DNT6nYjUVhKqDslNLy6iGHJJz85pgPcnxeY3ufcfXPuFeCnXkG",
#         "token_type": "Bearer",
#         "refresh_token": "1//0eHVZnWPDvz4MCgYIARAAGA4SNwF-L9Irtd4ByhFDbgWY03Pm7v43zHa1wCvIIDW6WL4C-hIxtdbRSZBLh0GylsFeV6KJvfui80g",
#         "expiry": "2021-08-14T12:43:23.1555349+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM9xWSG-IuqMsQEmKyylElTaEpsSTXLYtEmq-Pu44X4VxieLSX43sLJL7K7FCgofNo_Fbv2dx1byJrTdrUV1PrNu9wBafTDJ36rBQ686r5h2rLXj8gprrAk4htXxJF9Gd03znx4QvdnCgH4tv_HW2vuy",
#         "token_type": "Bearer",
#         "refresh_token": "1//0evDXFJHXWoalCgYIARAAGA4SNwF-L9IrxK2v87qQQ1G1wQNEMAkeltPaCgfAdRweCCY7esJrU6Lyd51bPbroeIpkOUaCEv87C7Y",
#         "expiry": "2021-08-14T12:43:47.849139+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM8J9lxK7373H1gIv3QYTZDJj1_EtJPqPmJ50cux9Kj8a3OBFAG8ffjBgaBXiWQogV_T-RdW4y70KW_oxk8TOY38tNQNofoZdpQnQxfje72mhq94M-f-n7paL6GtJzVhncfExxuUZHUh6yb4sI8qKeQS",
#         "token_type": "Bearer",
#         "refresh_token": "1//0eEZUpW1vnLSOCgYIARAAGA4SNwF-L9Irsws8wRe-hAlvecZKNmkfXCApqKyLt2E-65gmPYSK63SLQCY1OLsRSeT1jsTkA6ef4w4",
#         "expiry": "2021-08-14T12:45:07.0781638+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM9wtOXcWdIvBfLIrYqHNt8c0Uu8t6lOdSoRnWMhTM5H8T8-06YiFYZirIcQx3sZFtuqFFe5rjkHvml3P9kXiuBKa5eqJ4LYEWy2254lvFjt_8GX_qEGt6jllweuvBB2Q5yg31AeTU6zMx1m2MQQcYFp",
#         "token_type": "Bearer",
#         "refresh_token": "1//0en1_dyKImpETCgYIARAAGA4SNwF-L9IrdHX3u4-aRUJaVwRwZUQJ7Y1UwvoyWzKyvXPyK7bDzZzZzO68Z98P3hq0PqQ_p94L2jc",
#         "expiry": "2021-08-14T12:45:38.4772579+07:00"},
#     {
#         "access_token": "ya29.a0ARrdaM8SHTAam8kyXk-K-Hd2nGmFo1Fc1skFemDCkaB5ljTdNJhFZLpKmLc17F5sQVTUFl-eun4VrFfb8W2nnw7APtNUiV56FkbMUw-CnonbqkZrqIHzgpD_l4CFJltGnd0Vxr0EZmZeb9R9Kx1SqKb86l3_",
#         "token_type": "Bearer",
#         "refresh_token": "1//0eyXUSUwPgeY0CgYIARAAGA4SNwF-L9IrLbAf1owxBM3tFr3ePOZVX5OEtQCtjtxC6pYg1kd41--M3bhL5K9BJRfAqelx4BHNZmk",
#         "expiry": "2021-08-14T12:46:09.0011226+07:00"}
# ]
#
# list_return = []
#
# string_format = {
#     'email': 'id1',
#     'rclone_token': '{"access_token":"ya29.a0ARrdaM81b6k61sUGsTrO_aMZcow9yCTbqfoSBg3jFCIpYbidV-I4UiVr0hADhEraFNyoW05JWxBq2rlyeDd8FeRp0UXGIwW41vlgotgXfCBCGRbotwOQp5kHRzI7SdvKqGUVbVr0k6Xv9Ao0_bkp8xOim3yp","token_type":"Bearer","refresh_token":"1//0e1hMO-vPoNuoCgYIARAAGA4SNwF-L9IrEO6TpW0pABAUhQdc8Hh5INBIqL0xCOBNBm1YgpS2WWRbESD2XIiF77_jcs1tf6whyr4","expiry":"2021-08-18T11:59:13.3059316+07:00"}',
#     'share_drive_id': '0AJlOCO3IjHM_Uk9PVA'
# }
#
# for i in range(len(drive_list)):
#     list_return.append({
#         'email': 'id{}'.format(i),
#         'rclone_token': json.dumps(token_list[i]),
#         'share_drive_id': drive_list[i]
#     })
# print(list_return)
#
#
#
#
import time
import subprocess
import select
import os
filename = '/home/ty/.chia/mainnet/log/debug.log'
f = subprocess.Popen(['tail', '-F', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)
last_event_time = 0
while True:
    if int(time.time()) - last_event_time >= 10 * 60:
        os.system('/home/ty/stop_chia_script.sh')
        os.system('/home/ty/run_chia_script.sh')
        last_event_time = int(time.time())
    if p.poll(1):
        data = f.stdout.readline().decode()
        if 'harvester chia.harvester.harvester: INFO' in data or 'harvester chia.plotting.plot_tools: INFO' in data:
            print(data)
            last_event_time = int(time.time())
    time.sleep(0.01)
