#! coding:utf-8

def blob4path(dir_abs_path, Ext="*.wav"):
    """
    指定されたディレクトリからファイルパスのリストを取得
    :param dir_abs_path: ディレクトリパス
    :param Ext: 検索拡張子
    :return: 絶対パスのリスト [abs_path1, abs_paht2...]
    """

    import os, glob

    if not os.path.exists(dir_abs_path):
        raise StandardError("dir_abs_path is notting %s" % dir_abs_path)
    # 検索ワードの生成
    pathname = os.path.join(dir_abs_path, Ext)
    # print pathname
    # *.wavでファイルリストを取得
    wav_glob = glob.glob(pathname)
    # ファイル名を取得 : (ed)A04_J715_14B330_ch1.wav
    # wav_path_s = [os.path.basename(path) for path in wav_glob if os.path.isfile(path)]
    # 絶対パスの取得
    wav_abspath_s = [os.path.abspath(path) for path in wav_glob if os.path.isfile(path)]

    return wav_abspath_s