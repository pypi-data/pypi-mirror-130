# -*- coding: utf-8 -*-

import os
import shutil
import stat

class FileUtils:
    """FileUtils"""
    @staticmethod
    def open_lagre_file(filename:str):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                yield line

    @staticmethod
    def create_directory(directory:str) -> None:
        """创建目录"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def copy_dir(src:str, dst:str) -> None:
        """Recursively copy a directory tree.
        The destination directory must not already exist.
        If exception(s) occur, an Error is raised with a list of reasons."""

        if not os.path.exists(src):
            raise OSError("The source path does not exist! Please upload again!")
        if not os.path.exists(dst) and os.path.exists(src):
            shutil.copytree(src, dst)
        else:
            raise OSError("The target path already exists! After a minute retry ~!")

    @staticmethod
    def get_listdir(path:str) -> list:
        """遍历文件夹, 并返回当前文件夹下所有文件list"""
        if os.path.exists(path):
            value_list = os.listdir(path)
            return value_list
        else:
            raise OSError("The path %s does not exist!" % (path))

    @staticmethod
    def get_listdir_loop_01(path:str) -> list:
        """递归遍历文件夹, 并返回所有文件list(不含有文件夹)"""
        if os.path.exists(path):
            file_path_list = []
            for root, __, files in os.walk(path):
                file_path_list.extend(os.path.join(root, file) for file in files)
            return file_path_list
        else:
            raise OSError("The path %s does not exist!" % (path))

    @staticmethod
    def get_listdir_loop_02(path:str, file_type:str=True, dir_type:str=False) -> list:
        """遍历文件夹

        默认返回所有文件list(不含文件夹)；

        当file_type=True, dir_type=False； 则值返回文件列表；

        当file_type=Flase, dir_type=True 则值返文件夹列表；
        """
        if os.path.exists(path):
            file_path_list = []
            dir_path_list = []
            for root, dirs, files in os.walk(path):
                file_path_list.extend(os.path.join(root, f) for f in files)
                dir_path_list.extend(os.path.join(root, d) for d in dirs)
        else:
            raise OSError("The path %s does not exist!" % (path))

        if dir_type is False and file_type is True:
            return file_path_list
        elif dir_type is True and file_type is False:
            return dir_path_list
        elif dir_type is True and file_type is True:
            return file_path_list + dir_path_list
        else:
            raise ValueError("The dir_type/file_type is error!")

    @staticmethod
    def chown_user_perm(src:str, dst:str, loop=True) -> None:
        """文件/文件夹权限修改

            当loop等于True的时候,遍历文件夹。
        """
        if loop is True:
            all_list = FileUtils.get_listdir_loop_01(dst)
        else:
            all_list = FileUtils.get_listdir(dst)

        st = os.stat(src)
        if os.path.isdir(dst) and all_list is not None:
            for line in all_list:
                os.chown(line, st[stat.ST_UID], st[stat.ST_GID])
        else:
            raise OSError("The path %s is not exist!" % (dst))

    @staticmethod
    def rename_files(file_lists:list, file_prefix:any, file_suffix:int=None) -> None:
        """批量重命名文件
        
        file_prefix： 文件前缀，xxx-001.py; 默认不设置则保留原样
        file_suffix： 文件后缀，abc-00x.py, 默认不设置则保留原样

        file_lists = ["/root/1.py", "/root/a.py"]

        """
        if file_suffix is None or not str.isdigit(str(file_suffix)):
            uffix = 1
        else:
            uffix = file_suffix

        for f in file_lists:
            file_name, file_ext = os.path.splitext(f)
            if file_prefix is None:
                prefix = file_name
            else:
                prefix = file_prefix
            os.rename(f, prefix + str('{0:03}'.format(uffix)) + file_ext)
            uffix += 1

    @staticmethod
    def rename_file(old_file:str, new_file:str) -> None:
        """文件重命名

        参数:

            old_file：旧文件名；string。
            new_file：新文件名;string。
        """
        if not os.path.isfile(new_file):
            os.rename(old_file, new_file)
