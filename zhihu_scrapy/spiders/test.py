import zhihu_scrapy.tools as tools


def process_links_(links):
    """
    在Rule()获取到了各种links列表后，用此方法对其进行处理，
    :param links: Rule()获取到的links列表
    :return: 经过中间处理后的links列表
    """
    # todo 对links还未处理，会出现错误，待将每个信息的parse完成后再对此部分进行更新people
    new_links = set()
    for link in links:
        print(link)
        type_ = tools.url_type_select(link)
        if type_ in ["articles_"]:
            article_url_token = link.split("/")[-1]
            link = "".join(["https://zhuanlan.zhihu.com/api/posts/", article_url_token])
        else:
            pass
        new_links.update([link])
    return new_links


if __name__ == "__main__":
    # url = "https://www.zhihu.com/people/stevenjohnson/answers"
    # url_splited = url.split("/")
    # length_of_url_splited = len(url_splited)
    # print(url_splited)
    # print(length_of_url_splited)
    url = "https://www.zhihu.com/question/52750322#answer-48316476"
    # url = "https://www.zhihu.com/question/52750322"
    url = 'https://www.zhihu.com/question/35931586/answer/131875262'
    print(url.split("answer"))
