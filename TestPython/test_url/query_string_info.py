__author__ = 'R.Azh'


class QueryStringInfo:
    skip = None
    take = None
    search_text = None
    sort = None
    operator = None
    criteria = None

    def __init__(self, default_operator="or", default_sort={'_id': -1}, default_take=150, default_skip=0):
        self.operator = default_operator
        self.sort = default_sort
        self.take = default_take
        self.skip = default_skip

    def load(self, query_string, check_criteria_emptiness=False):
        # query_string_fetch_validation = QueryStringFetchValidation()
        # query_string_fetch_validation.validate(query_string)

        # if check_criteria_emptiness:
        #     query_string_criteria_emptiness_validation = QueryStringCriteriaEmptinessValidation()
        #     query_string_criteria_emptiness_validation.validate(query_string)

        if "skip" in query_string:
            self.skip = int(query_string["skip"])

        if "take" in query_string:
            self.take = int(query_string["take"])

        if "search_text" in query_string:
            self.search_text = query_string["search_text"]

        if "sort" in query_string:
            self.load_sort(query_string)

        if "operator" in query_string:
            self.operator = query_string["operator"]

        if "criteria" in query_string:
            self.load_criteria(query_string)

        if "ids" in query_string:
            self.load_ids(query_string)

    def load_sort(self, query_string):
        if query_string and query_string["sort"]:
            self.sort = {}
            sort_item = query_string["sort"]
            sort_list = sort_item.split(",")
            for sort_item in sort_list:
                sort_order_sign = sort_item[0:1]
                if sort_order_sign == "-":
                    sort_field_name = sort_item[1:]
                    self.sort[sort_field_name] = -1
                else:
                    self.sort[sort_item] = 1

    def load_criteria(self, query_string):
        if query_string and query_string["criteria"]:
            # query_string_criteria_emptiness_validation = QueryStringCriteriaEmptinessValidation()
            # query_string_criteria_emptiness_validation.validate(query_string)
            self.criteria = []
            criteria_item = query_string["criteria"]
            criteria_list = criteria_item.split(",")
            for criteria_item in criteria_list:
                if ":" in criteria_item:
                    criteria_item_list = criteria_item.split(":")
                    criteria_field_name = criteria_item_list[0]
                    criteria_field_value = criteria_item_list[1]
                    self.criteria.append((criteria_field_name, criteria_field_value))
                elif "<" in criteria_item:
                    criteria_item_list = criteria_item.split("<")
                    criteria_field_name = criteria_item_list[0]
                    criteria_field_value = criteria_item_list[1]
                    self.criteria.append((criteria_field_name, "<{}".format(criteria_field_value)))
                elif ">" in criteria_item:
                    criteria_item_list = criteria_item.split(">")
                    criteria_field_name = criteria_item_list[0]
                    criteria_field_value = criteria_item_list[1]
                    self.criteria.append((criteria_field_name, ">{}".format(criteria_field_value)))
                elif "<=" in criteria_item:
                    criteria_item_list = criteria_item.split("<=")
                    criteria_field_name = criteria_item_list[0]
                    criteria_field_value = criteria_item_list[1]
                    self.criteria.append((criteria_field_name, "<={}".format(criteria_field_value)))
                elif ">=" in criteria_item:
                    criteria_item_list = criteria_item.split(">=")
                    criteria_field_name = criteria_item_list[0]
                    criteria_field_value = criteria_item_list[1]
                    self.criteria.append((criteria_field_name, ">={}".format(criteria_field_value)))
                elif "=" in criteria_item:
                    criteria_item_list = criteria_item.split("=")
                    criteria_field_name = criteria_item_list[0]
                    criteria_field_value = criteria_item_list[1]
                    self.criteria.append((criteria_field_name, format(criteria_field_value)))

    def load_ids(self, query_string):
        if query_string and query_string["ids"]:
            # query_string_ids_emptiness_validation = QueryStringIdsEmptinessValidation()
            # query_string_ids_emptiness_validation.validate(query_string)
            self.ids = []
            ids_item = query_string['ids']
            ids_list = ids_item.split(",")
            [self.ids.append(id) for id in ids_list]


def build_dynamic_sql_alchemy_query(query_string):
    query_string_info = QueryStringInfo()
    query_string_info.load(query_string)
    print(query_string_info.__dict__)
    # search(query_string_info.search_text, query_string_info.skip, query_string_info.take, query_string_info.sort)

    # def search(self, search_text, skip, take, sort={'title': 1}):
    #     from sqlalchemy import text
    #     from sqlalchemy.sql.expression import desc
    #     query = School.query   # sqlalchemy model class
    #     if search_text:
    #         query = query.filter(text("title ~'.*{}.*'".format(search_text)))
    #     for key, value in sort.items():
    #         if value == 1:
    #             query = query.order_by(getattr(School, key))
    #         else:
    #             query = query.order_by(desc(getattr(School, key)))
    #     query = query.offset(skip).limit(take)
    #     return query.all()

url = "http://amir.parsadp.com/api/v1.0/persons/advanced_search?skip=5&operator=and&sort=name%2C-last_name&criteria" \
      "=experience_company_name%3Agoogle%2Cexperience_title%3Aexperience&take=130"
import urllib.parse as urlparse
url_parts = list(urlparse.urlparse(url))
query = dict(urlparse.parse_qsl(url_parts[4]))
build_dynamic_sql_alchemy_query(query)

#
# criteria = (('UserID', 2), ('ConvoID', 1) ,('ContactID', 353))
#
# query = session.query(tablename)
# for _filter, value in criteria:
#     query = query.filter(getattr(tablename, _filter) == value)
# result = query.all()