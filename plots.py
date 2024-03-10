import matplotlib.pyplot as plt


def tikzplotlib_fix_ncols(obj):
    """
    workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, which breaks tikzplotlib
    """
    if hasattr(obj, "_ncols"):
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)


def state_increase(value_to_plot='steps'):
    ll_ls_time, ll_ls_queries, ll_ls_steps = [0.0475, 0.0516, 0.0249, 0.032, 0.0453, 0.0538, 0.060399999999999995,
                                              0.06659999999999999, 0.0674, 0.0801, 0.0781, 0.0926, 0.1072,
                                              0.13779999999999998, 0.09759999999999999, 0.1049, 0.1004,
                                              0.13979999999999998, 0.1252, 0.145], [2930.5, 6209.0, 8937.8, 12263.5,
                                                                                    15604.8, 18374.6, 22951.1, 24784.7,
                                                                                    28298.3, 31113.0, 34536.3, 38974.3,
                                                                                    41968.9, 46564.2, 48616.5, 52527.0,
                                                                                    55151.9, 62634.1, 59748.6,
                                                                                    67544.0], [19897.4, 51135.6,
                                                                                               69844.9, 95850.4,
                                                                                               130109.2, 145357.0,
                                                                                               190977.5, 213698.3,
                                                                                               219377.5, 250127.4,
                                                                                               277093.2, 346211.0,
                                                                                               367292.0, 404789.2,
                                                                                               417370.0, 479273.0,
                                                                                               475196.4, 639050.1,
                                                                                               554836.8, 630958.6]
    ll_kv_time, ll_kv_queries, ll_kv_steps = [0.0382, 0.053500000000000006, 0.028999999999999998, 0.0403, 0.0517,
                                              0.0849, 0.06860000000000001, 0.081, 0.0938, 0.1079, 0.10389999999999999,
                                              0.1071, 0.1328, 0.1558, 0.1271, 0.1332, 0.1347, 0.1451, 0.1535, 0.1716], [
                                                 1801.1, 4040.8, 6302.0, 8711.6, 11049.4, 13807.8, 16083.2, 18756.6,
                                                 21534.1, 24408.5, 26703.7, 28715.1, 31734.0, 34569.3, 37771.7, 40864.5,
                                                 45531.7, 46230.3, 48053.1, 51236.6], [26418.8, 59773.6, 98419.6,
                                                                                       139889.4, 183480.8, 235416.3,
                                                                                       270375.3, 325764.9, 371755.9,
                                                                                       418855.8, 459795.1, 496390.7,
                                                                                       558075.1, 613540.9, 658999.1,
                                                                                       724496.4, 814710.9, 840127.7,
                                                                                       861125.2, 943909.5]
    ll_ttt_time, ll_ttt_queries, ll_ttt_steps = [0.0511, 0.06, 0.042499999999999996, 0.0827, 0.086, 0.1523, 0.1399,
                                                 0.1806, 0.22139999999999999, 0.25139999999999996, 0.2747, 0.3093,
                                                 0.4048999999999999, 0.5229, 0.3975, 0.3967, 0.4206,
                                                 0.49539999999999995, 0.5942000000000001, 0.6505], [1983.0, 4285.2,
                                                                                                    6797.8, 9297.3,
                                                                                                    11954.1, 14508.9,
                                                                                                    17208.4, 19886.8,
                                                                                                    22684.4, 25442.1,
                                                                                                    28343.9, 31131.3,
                                                                                                    33993.7, 36699.2,
                                                                                                    39870.9, 42707.7,
                                                                                                    45566.2, 48587.6,
                                                                                                    51535.3, 54435.1], [
                                                    13363.2, 32310.2, 58556.9, 85409.0, 110334.2, 140237.5, 171893.0,
                                                    201348.8, 247288.9, 268712.5, 305542.7, 349206.7, 383979.6,
                                                    454796.7, 449359.9, 504025.5, 540138.9, 569689.4, 638495.0,
                                                    673561.4]

    al_ls_time, al_ls_queries, al_ls_steps = [0.02, 0.035, 0.053000000000000005, 0.067, 0.092, 0.086, 0.122, 0.184,
                                              0.173, 0.187, 0.182, 0.218, 0.28200000000000003, 0.309,
                                              0.28200000000000003, 0.286, 0.31, 0.412, 0.412, 0.481], [2911.4, 6402.4,
                                                                                                       10305.6, 13811.5,
                                                                                                       18842.4, 21631.2,
                                                                                                       26001.9, 30419.7,
                                                                                                       32805.3, 38078.6,
                                                                                                       40579.6, 47094.5,
                                                                                                       51999.5, 55948.2,
                                                                                                       57368.3, 62264.2,
                                                                                                       65068.7, 73482.9,
                                                                                                       77398,
                                                                                                       84963.7], [
                                                 15237.7, 36300.9, 62287.7, 85816, 122367.9, 141892.5, 172942.7, 207286,
                                                 223415.6, 264726.2, 283978.5, 333102.6, 371415.3, 401845.5, 419710.3,
                                                 454457.6, 478511.3, 541199.3, 573384.7, 637043.6]

    al_ls_cpython_time = [0.035, 0.048, 0.103, 0.153, 0.241, 0.257, 0.379, 0.391, 0.419, 0.535, 0.5690000000000001, 0.705, 0.744, 0.72, 0.773, 0.952, 0.998, 1.074, 1.023, 1.191]


    al_kv_time, al_kv_queries, al_kv_steps = [0.044000000000000004, 0.055, 0.08700000000000001, 0.132, 0.126, 0.17,
                                              0.194, 0.23500000000000001, 0.28600000000000003, 0.33, 0.485, 0.492,
                                              0.514, 0.548, 0.628, 0.703, 0.753, 0.9390000000000001, 1.035, 0.978], [
                                                 1682.2, 3680.3, 5959.6, 8129.9, 10610.4, 12969.9, 15247.3, 17831.1,
                                                 20155.1, 22919.1, 25585.3, 27595.1, 30383.1, 33091, 35399.9, 38781.2,
                                                 40640.8, 43171.5, 46103.4, 49336.1], [10397.8, 24182.4, 41190.2,
                                                                                       58169.5, 78150.3, 97872.9,
                                                                                       114901.1, 136392, 157084.6,
                                                                                       178374.8, 202017.8, 223225,
                                                                                       247525.2, 270261.1, 288816.6,
                                                                                       319297.6, 339456.8, 363290.3,
                                                                                       394449.5, 413042.1]

    al_kv_cpython_time = [0.031, 0.07, 0.10400000000000001, 0.17900000000000002, 0.241, 0.269, 0.384, 0.402, 0.508, 0.556, 0.797, 0.876, 0.907, 0.997, 1.141, 1.267, 1.444, 1.483, 1.678, 2.097]

    if value_to_plot == 'steps':
        ll_ls, ll_kv, ll_ttt, al_ls, al_kv = ll_ls_steps, ll_kv_steps, ll_ttt_steps, al_ls_steps, al_kv_steps
    elif value_to_plot == 'time':
        ll_ls, ll_kv, ll_ttt, al_ls, al_kv = ll_ls_time, ll_kv_time, ll_ttt_time, al_ls_cpython_time, al_kv_cpython_time
    else:
        ll_ls, ll_kv, ll_ttt, al_ls, al_kv = ll_ls_queries, ll_kv_queries, ll_ttt_queries, al_ls_queries, al_kv_queries

    model_sizes = list(range(100, 2001, 100))

    plt.plot(model_sizes, ll_ls, label='L* (LearnLib)')
    plt.plot(model_sizes, ll_kv, label='KV (LearnLib)')
    plt.plot(model_sizes, ll_ttt, label='TTT (LearnLib)')

    plt.plot(model_sizes, al_ls, label='L* (AALpy)')
    plt.plot(model_sizes, al_kv, label='KV (AALpy)')

    # if value_to_plot == 'time':
    #     plt.plot(model_sizes, al_ls_cpython_time, label='L* (AALpy, Cpython)')
    #     plt.plot(model_sizes, al_kv_cpython_time, label='KV (AALpy, Cpython)')

    plt.xlabel('Model Size')
    if value_to_plot == 'time':
        plt.ylabel('Learning Time (seconds)')
    elif value_to_plot == 'steps':
        plt.ylabel('Learning Steps')
    else:
        plt.ylabel('Learning Queries')

    plt.grid()
    plt.legend()
    #plt.show()

    tikzplotlib_fix_ncols(plt.legend())
    import tikzplotlib
    tikzplotlib.save(f"increasing_model_size_comp_{value_to_plot}.tex")


def alphabet_increase(value_to_plot='steps'):
    # L star, 250 states, alph until 50
    ll_ls_time, ll_ls_queries, ll_ls_steps = [0.0225, 0.1068, 0.3123, 0.6143, 0.9353, 1.7116, 2.2936, 3.308, 4.4742,
                                              5.975], [20010.0, 80020.0, 180030.0, 320040.0, 500050.0, 720060.0,
                                                       980070.0, 1280080.0, 1620090.0, 2000100.0], [90550.0, 323260.0,
                                                                                                    695550.0, 1219240.0,
                                                                                                    1885300.0,
                                                                                                    2688540.0,
                                                                                                    3625580.0,
                                                                                                    4691280.0,
                                                                                                    5882310.0,
                                                                                                    7198100.0]

    ll_kv_time, ll_kv_queries, ll_kv_steps = [0.023, 0.0581, 0.12789999999999999, 0.1807, 0.2319, 0.3639,
                                              0.43100000000000005, 0.5562, 0.5993999999999999, 0.8317], [7740.0,
                                                                                                         15057.4,
                                                                                                         22692.8,
                                                                                                         29684.8,
                                                                                                         36590.3,
                                                                                                         44002.3,
                                                                                                         51569.1,
                                                                                                         60684.0,
                                                                                                         64439.9,
                                                                                                         75561.2], [
                                                 109935.2, 223465.5, 354824.3, 470441.1, 587552.2, 724908.3, 857161.9,
                                                 996200.1, 1047168.2, 1254155.2]
    ll_ttt_time, ll_ttt_queries, ll_ttt_steps = [0.023200000000000002, 0.0508, 0.0963, 0.1472, 0.1824, 0.2866,
                                                 0.30670000000000003, 0.3892, 0.4671, 0.5576], [9314.7, 19321.3,
                                                                                                29237.0, 38968.5,
                                                                                                49164.0, 58989.8,
                                                                                                68778.8, 78890.7,
                                                                                                88673.3, 98802.4], [
                                                    63948.0, 121652.7, 182578.9, 243704.5, 313167.7, 379247.5, 472159.4,
                                                    498109.3, 570811.1, 632522.9]

    al_ls_time, al_ls_queries, al_ls_steps = [0.060000000000000005, 0.163, 0.328, 0.627, 0.857, 0.937, 1.279, 1.609,
                                              2.094, 2.6630000000000003], [20000, 80000, 180000, 320000, 500000, 720000,
                                                                           980000, 1280000, 1620000, 2000000], [90540,
                                                                                                                323240,
                                                                                                                695520,
                                                                                                                1219200,
                                                                                                                1885250,
                                                                                                                2688480,
                                                                                                                3625510,
                                                                                                                4691200,
                                                                                                                5882220,
                                                                                                                7198000]
    al_ls_cpython_time = [0.189, 0.612, 1.408, 2.393, 3.558, 5.342, 6.912, 8.984, 11.817, 14.281]

    al_kv_time, al_kv_queries, al_kv_steps = [0.10200000000000001, 0.115, 0.175, 0.157, 0.228, 0.28200000000000003,
                                              0.346, 0.364, 0.447, 0.5609999999999999], [7775.7, 15697, 23651, 31452,
                                                                                         39253.8, 47259.5, 55460.1,
                                                                                         63576.6, 71087.2, 79622.1], [
                                                 42556.7, 76230.2, 108281.1, 142432.8, 170925.2, 204147.5, 237700.1,
                                                 264808.1, 299299.2, 332669.8]

    al_kv_cpython_time = [0.106, 0.20700000000000002, 0.263, 0.445, 0.498, 0.548, 0.758, 0.75, 0.756, 0.846]


    if value_to_plot == 'steps':
        ll_ls, ll_kv, ll_ttt, al_ls, al_kv = ll_ls_steps, ll_kv_steps, ll_ttt_steps, al_ls_steps, al_kv_steps
    elif value_to_plot == 'time':
        ll_ls, ll_kv, ll_ttt, al_ls, al_kv = ll_ls_time, ll_kv_time, ll_ttt_time, al_ls_cpython_time, al_kv_cpython_time
    else:
        ll_ls, ll_kv, ll_ttt, al_ls, al_kv = ll_ls_queries, ll_kv_queries, ll_ttt_queries, al_ls_queries, al_kv_queries

    model_sizes = list(range(10, 101, 10))

    plt.plot(model_sizes, ll_ls, label='L* (LearnLib)')
    plt.plot(model_sizes, ll_kv, label='KV (LearnLib)')
    plt.plot(model_sizes, ll_ttt, label='TTT (LearnLib)')

    plt.plot(model_sizes, al_ls, label='L* (AALpy)')
    plt.plot(model_sizes, al_kv, label='KV (AALpy)')

    # if value_to_plot == 'time':
    #     plt.plot(model_sizes, al_ls_cpython_time, label='L* (AALpy, Cpython)')
    #     plt.plot(model_sizes, al_kv_cpython_time, label='KV (AALpy, Cpython)')

    plt.xlabel('Alphabet Size')
    if value_to_plot == 'time':
        plt.ylabel('Learning Time (seconds)')
    elif value_to_plot == 'steps':
        plt.ylabel('Learning Steps')
    else:
        plt.ylabel('Learning Queries')

    plt.grid()
    plt.legend()
    #plt.show()

    tikzplotlib_fix_ncols(plt.legend())
    import tikzplotlib
    tikzplotlib.save(f"increasing_alph_size_comp_{value_to_plot}.tex")


def plot_real():
    # LS_LL, LS_LV, LS_TTT, LS_AL, KV_AL
    tcp_ubuntu_steps = [16116.7, 5809.2, 2949.7, 9346, 3256.7]
    verne_steps = [24906.2, 8254.7, 3082.5, 14216.2, 3887.1]
    mosquito_steps = [24398.1, 8465.9, 3341.0, 15021.2, 4037.4]
    abs_channel = [5522208.0, 1201427.1, 74551.8, 5522085, 46924.1]

    # Index names
    index_names = ['L*\n (LearnLib)', 'KV\n (LearnLib)', 'TTT\n (LearnLib)', 'L*\n (AALpy)', 'KV\n (AALpy)']

    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Color scheme
    colors = ['blue', 'orange', 'green', 'red', 'purple']

    # Plot 1
    axs[0, 0].bar(index_names, tcp_ubuntu_steps, color=colors)
    axs[0, 0].set_title('TCP Ubuntu Client')

    # Plot 2
    axs[0, 1].bar(index_names, verne_steps, color=colors)
    axs[0, 1].set_title('Verne MQTT')

    # Plot 3
    axs[1, 0].bar(index_names, mosquito_steps, color=colors)
    axs[1, 0].set_title('Mosquito MQTT')

    # Plot 4
    axs[1, 1].bar(index_names, abs_channel, color=colors)
    axs[1, 1].set_title('ABS Channel Frame')

    # for ax in axs.flat:
    #     ax.set_xticklabels(index_names, rotation=90)

    # Adjust layout
    plt.tight_layout()
    # plt.subplots_adjust(hspace=0.5)

    # tikzplotlib_fix_ncols(plt.legend())
    import tikzplotlib
    tikzplotlib.save(f"comparison_real_world.tex")

    # Show plots
    # plt.show()


def plot_non_det():
    non_det_steps_n_5 = [83066.86666666667, 221363.2, 428500.93333333335, 670301.5333333333, 1183972, 1689262.2666666666, 1753791.2666666666, 2692857.2, 2550680.933333333, 3353361.8666666667]

    model_size = list(range(5, 51, 5))

    plt.plot(model_size, non_det_steps_n_5)

    plt.show()

def plot_rpni():
    dataset_sizes = list(range(5000, 50001, 5000))
    dataset_sizes.insert(0, 1000)

    runtime_pta = [0.07,0.53,0.94,1.5,2.2,2.63,3.14,4.43, 4.59,5.03,5.64]
    runtime_rpni = [0.9, 0.88, 1.46, 2.08, 3.13, 3.26, 4.62, 5.38, 5.6, 7.07, 6.68]

    memory = [9.17, 41.649200439453125, 80.55925750732422, 118.72746276855469, 158.91128540039062, 195.97640991210938, 232.49866485595703, 271.40914154052734, 307.3223419189453, 343.73868560791016, 378.8228988647461, 604.4000396728516, ]

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plotting runtime data
    plt.subplot(1, 2, 1)
    plt.plot(dataset_sizes, runtime_pta, marker='o', label='PTA Construction Time')
    plt.plot(dataset_sizes, runtime_rpni, marker='x', label='RPNI Runtime')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    tikzplotlib_fix_ncols(plt.legend())
    # Plotting memory data
    plt.subplot(1, 2, 2)
    plt.plot(dataset_sizes, memory, marker='s', color='red')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory (MB)')

    #plt.tight_layout()
    # plt.show()


    import tikzplotlib
    tikzplotlib.save(f"rpni_evaluation.tex")

def plot_alergia():
    dataset_sizes = list(range(5000, 50001, 5000))
    dataset_sizes.insert(0, 1000)

    runtime_fppta = [ 0.03,0.27, 0.65,1.26,2.3, 2.34,2.36,2.62,2.79,3.05,4.82]
    runtime_alergia = [0.14,0.65,1.74,2.32,3.26, 3.35,3.82,4.38,4.22,4.47,4.58]

    memory = [16.931365966796875, 80.29080963134766, 158.60912322998047, 238.66165161132812, 303.0407180786133, 364.36720275878906, 441.9717330932617, 503.41678619384766,604.4000396728516, 641.6547927856445, 637.2552947998047]
    # Plotting
    plt.figure(figsize=(12, 6))

    # Plotting runtime data
    plt.subplot(1, 2, 1)
    plt.plot(dataset_sizes, runtime_fppta, marker='o', label='PTA Construction Time')
    plt.plot(dataset_sizes, runtime_alergia, marker='x', label='Alergia Runtime')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    tikzplotlib_fix_ncols(plt.legend())
    # Plotting memory data
    plt.subplot(1, 2, 2)
    plt.plot(dataset_sizes, memory, marker='s', color='red')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory (MB)')

    #plt.tight_layout()
    # plt.show()

    import tikzplotlib
    tikzplotlib.save(f"alergia_evaluation.tex")


# plot_alergia()
# plot_rpni()
# plot_non_det()
# plot_real()
#alphabet_increase(value_to_plot='queries')
state_increase(value_to_plot='time')
