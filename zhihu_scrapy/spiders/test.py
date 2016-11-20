import zhihu_scrapy.tools as tools


def process_links_(links):
    """
    在Rule()获取到了各种links列表后，用此方法对其进行处理，
    :param links: Rule()获取到的links列表
    :return: 经过中间处理后的links列表
    """
    # todo 对links还未处理，会出现错误，待将每个信息的parse完成后再对此部分进行更新
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
    url = ["https://zhuanlan.zhihu.com/p/23250032",
           "https://zhuanlan.zhihu.com/p/2325032"]
    print(process_links_(url))
