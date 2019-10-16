import xlwt
import xlrd
import os
from xlutils.copy import copy as xl_copy


class EXCEL(object):
    def __init__(self, path, sheet_names):
        self.header = ['序号', '标题', '创建时间', '关键词', '链接', '备注']
        self.col_width = [1500, 14000, 4000, 4000, 10000, 10000]
        self.base_path = path
        self.sheet_names = sheet_names if bool(sheet_names) else ['All']
        self.save_num = 0

        if not os.path.exists(self.base_path):
            self.create_excel()

        self.wb = self.get_excel()

    def create_excel(self):
        wb = xlwt.Workbook()
        [self.add_new_sheet(sheet_name, wb) for sheet_name in self.sheet_names]
        wb.save(self.base_path)

    def add_new_sheet(self, sheet_name, wb):
        sheet = wb.add_sheet(sheet_name, cell_overwrite_ok=True)
        [sheet.write(0, i, self.header[i], self.set_style(bold=True))
         for i in range(len(self.header))]
        for i, w in enumerate(self.col_width):
            sheet.col(i).width = w

    def get_excel(self):
        # 添加新sheet
        rb = self.open_workbook()
        wb = xl_copy(rb)
        [self.add_new_sheet(name, wb) for name in self.sheet_names if name not in rb.sheet_names()]
        wb.save(self.base_path)
        return wb

    def write_excel(self, new_papers):
        for data in new_papers:
            keywords = data['keywords'] if bool(data['keywords']) else ['All']
            for k in keywords:    # 按关键词存入，可以一文多存
                rb = self.open_workbook()
                old_paper_titles = [x.split('\n')[0].strip().lower()
                                    for x in rb.sheet_by_name(k).col_values(1)[1:]]

                if data['title'].strip().lower() not in old_paper_titles:     # 去重
                    self.save_num += 1
                    papers = self.data_sort(rb, k, data)    # 排序
                    self.write_new_row(k, papers)

                self.wb.save(self.base_path)

    def write_new_row(self, sheet_name, papers):
        for index, data in enumerate(papers):
            sheet = self.wb.get_sheet(sheet_name)
            data.insert(0, index+1)
            for i in range(len(data)):
                underline = True if i == 4 else False
                ali = False if i == 5 else True
                if bool(data[-1]) and i == 1:
                    p_colour = 5
                else:
                    p_colour = 1

                sheet.write(index+1, i, data[i],
                            self.set_style(underline=underline, ali=ali, pattern_colour=p_colour))

    def data_sort(self, rb, name, data):
        new_paper = [data['title'] + '\n' + data['title_ch'],
                     data['time'], ','.join(data['keywords']),
                     data['link'], data['annotation']]
        sheet = rb.sheet_by_name(name)
        nrows = sheet.nrows
        papers = [sheet.row_values(i)[1:] for i in range(1, nrows)]
        papers.append(new_paper)
        return sorted(papers, key=lambda x: x[1], reverse=True)

    def open_workbook(self):
        return xlrd.open_workbook(self.base_path, formatting_info=True)

    def set_style(self, name='宋体', height=220, bold=False, underline=False, ali=True, colour=0, pattern_colour=1):
        # 设置表格样式
        # 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 22 = Light Gray
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.underline = underline
        font.height = height
        font.weight = 512
        font.colour_index = colour

        alignment = xlwt.Alignment()
        if ali:
            alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        alignment.wrap = 1

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = pattern_colour

        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left_colour = 22
        borders.right_colour = 22
        borders.top_colour = 22
        borders.bottom_colour = 22

        style = xlwt.XFStyle()
        style.font = font
        style.alignment = alignment
        style.pattern = pattern
        style.borders = borders
        return style