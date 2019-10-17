
# 示例
# def getPMsgList(id, recPerPage):
#     List = Paginator(p_message.objects.filter(m_f_id=id).values().order_by('create_time'), recPerPage)
#     return List
# 传入已经查询到的分页，会自动生成含有分页数据的对象

class PageObject:
    def __init__(self):
        self.data = None

    # 分页查询
    def handlePage(self, mgsLsit, page, recPerPage):

        # 获取当前页码的数据
        page_list = mgsLsit.page(page)

        # 查询是否有上页下页
        try:
            next_page = page_list.next_page_number()
        except:
            next_page = False

        try:
            pre_page = page_list.previous_page_number()
        except:
            pre_page = False
        rangeList = list(mgsLsit.page_range)
        page_range = []

        # 分页区间规则
        if page > 4 and page < len(rangeList) - 3:
            if len(rangeList) > 6:
                rangeList = [rangeList[0], False, page - 1, page, page + 1,
                             False, rangeList[len(rangeList) - 1]]

        elif page >= len(rangeList) - 3:
            if len(rangeList) > 6:
                rangeList = [rangeList[0], False, rangeList[len(rangeList) - 5], rangeList[len(rangeList) - 4],
                             rangeList[len(rangeList) - 3],
                             rangeList[len(rangeList) - 2], rangeList[len(rangeList) - 1]]
            else:
                for item in rangeList:
                    page_range.append(item)
                rangeList = page_range

        else:
            if len(rangeList) > 6:
                rangeList = [rangeList[0], rangeList[1], rangeList[2], rangeList[3], rangeList[4],
                             False, rangeList[len(rangeList) - 1]]
            else:
                for item in rangeList:
                    page_range.append(item)
                rangeList = page_range

        # 生成分页对象
        pageData = {
            'rec_per_page': recPerPage,
            'now_page': page,
            'count': mgsLsit.count,
            'num_pages': mgsLsit.num_pages,
            'page_range': rangeList,
            'has_previous': page_list.has_previous(),
            'has_next': page_list.has_next(),
            'next_page': next_page,
            'pre_page': pre_page,
            'page_list': list(page_list)
        }
        return pageData
