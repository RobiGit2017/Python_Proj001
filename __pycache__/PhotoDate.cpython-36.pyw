3
��ZZ   �               @   s|   d Z ddlZddlZddlZddlZddlZdd� Zdd� Zdd� Z	dd	d
�Z
ddd�Zddd�Zdd� Zedkrxe�  dS )u�  
Date: 2017/11/07
Author: Robi

Target:
    獲得圖片檔EXIF(Exchangeable image file format)資訊進行自動化檔名修改
    for JPEG、TIFF、RIFF
info:
    exifread:
        https://pypi.python.org/pypi/ExifRead
        http://www.exiv2.org/tags.html
reference: 
    https://docs.python.org/3/library/os.html?highlight=os#module-os
    https://www.ricequant.com/community/topic/2027/
�    Nc              C   s   t j� } | S )N)�
filedialog�askopenfilename)�	file_path� r   �.Z:\FTP\Python_Proj001\Source code\PhotoDate.py�GuiGet   s    r   c              C   s   d} t j d|  �}|S )N�JPGz./*.)�glob)�temp�filesr   r   r   �FilePath)   s    r   c             C   s�   t j| �}tjdtj|j��}tjdtj|j��}t| d�}tj	|�}t
|d �}|jd�}|d jd�|d jd�dd�  }|jd	d
� dj|�}|||fS )Nz%Y%m%d-%H%M�rbzEXIF DateTimeOriginal� r   �:�   �   �   �-� )�os�stat�time�strftime�	localtime�st_ctime�st_mtime�open�exifread�process_file�str�split�insert�join)�file�info�date_c�date_m�fid_rb1�tagsr
   �date_or   r   r   �	PhotoTime0   s    



$
r*   c             C   s�   dd� | D �}g }x4t dt|��D ]"}|j|| | d ||  � q"W ddddd	g}tj|t dt|��|d gd
�}tj|t dt|��|d gd
�}tj|t dt|��|dd� d
�}	tj|||	gdddd�}
d}|
j|ddd� dS )Nc             S   s   g | ]}t jj|��qS r   )r   �path�basename)�.0�xr   r   r   �
<listcomp>P   s    zNakeLog.<locals>.<listcomp>r   �_u   檔案名稱u   原始名稱u   拍攝日期u   建立日期u   編輯日期)�index�columnsr   r   �   F�outer)�axis�ignore_indexr"   z
./Info.csv�,�ansi)�sep�encoding)�range�len�append�pd�	DataFrame�concat�to_csv)r   �dates�sel�filename�name_new�n�title�df1�df2�df3�res_df�	file_namer   r   r   �NakeLogM   s    "  "rM   r   c             C   s"  t j| dd�}t||jd  �}t||jd  �}|dkr�d}tjd| d � x�tdt|��D ]V}tjd	||  d
 | d ||  d � td	||  d
 | d ||  d � q`W nbtj	� }xXtdt|��D ]F}tjd||  d
 ||  d � td||  d
 ||  d � q�W dS )Nr8   )r:   r   r   �resultzmd "./�"r   zcopy "./z" "./�/z" /Y/Vzmove /-Y "./)
r>   �read_csv�listr2   r   �systemr;   r<   �print�getcwd)r   �duplication�data_dfrE   rD   �folderrF   r   r   r   �ReFilee   s    *."$rY   r   c       	      C   s  t j| dd�}t||jd  �}dd� |D �}t|�}x�|D ]�}tjd| d � x�t|d�D ]�\}}||kr^|j| |jd	  }|d
kr�tjd| d | d d � t	d| d | d d � q^tjd| d | d � t	d| d | d � q^W q<W dS )Nr8   )r:   r   c             S   s   g | ]}|d |j d�� �qS )Nr   )�find)r-   r.   r   r   r   r/   |   s    ztoFolder.<locals>.<listcomp>zmd "./rO   r   r   r   zcopy "./z" "./rP   z" /Y/Vzmove /-Y "./z/")
r>   rQ   rR   r2   �setr   rS   �	enumerate�locrT   )	r   rV   rW   �date_idx�date_set�fmdrF   �idxr#   r   r   r   �toFolderx   s    
 rb   c              C   s�   t � } t| �dkrtd� dS x*tdt| ��D ]}td| |  dd� q.W g }x| D ]}t|�}|j|� qTW t| |dd� d}t|d	d
� dS )Nr   zNo Filer   z%s�
)r9   )rC   z
./Info.csvr   )rV   )r   r<   rT   r;   r*   r=   rM   rb   )r   rF   rB   r#   �date�	Info_pathr   r   r   �main�   s    
rf   �__main__)r   )r   )r   )�__doc__r   r	   r   r   �pandasr>   r   r   r*   rM   rY   rb   rf   �__name__r   r   r   r   �<module>   s   


