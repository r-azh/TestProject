import sys

sys.path.insert(0, '/var/www/venv/IPN-Core')
sys.path.insert(0, '/var/www/venv/IPN-App/IPN')

__author__ = 'R.Azh'

from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient


def create_post_comment_like_from_old_db():
    posts = []
    comments = []
    likes = []
    dbClient = MongoClient('localhost', 27017)
    db = dbClient.ipn_db
    # deserializer = Deserializer()

    def create_post_from_company_post(documents):
        from parsadp.ipn.domain.aggregates.post.model.post import Post

        results = []
        if documents:
            for document in documents:
                # document = deserializer.deserialize_from_dictionary(json_dictionary=document, dumper=json_util)
                post = Post()
                post._id = ObjectId(document['_id'])
                post.title = document['subject']
                post.text = document['description']
                post.creator = create_post_creator(document['creator'])
                post.publish_datetime = document['created_date']
                post.file = document['file']
                post.file_thumbnail = document['file_thumbnail']
                post.container_id = document['company']['_id']
                post.container_type = 'companies'
                post.container_info = create_company_from_dict(document['company'])
                post.is_admin_post = str(document['creator']['person_id']) == "5601216789562c13d4567f0a"
                post.users_who_removed_admin_shares = []
                post.like_count = document['like_count'] #len(document['likes'])
                post.comment_count = comment_count(post._id, 'company_posts')
                post.viewer_count = 0
                if document['likes']:
                    create_like_from_post_likes(document['likes'], 'companies', document['company']['_id'], document['_id'])
                results.append(post)
                print("company_post: ", post._id)
        return results

    def create_post_from_group_post(documents):
        from parsadp.ipn.domain.aggregates.post.model.post import Post

        results = []
        if documents:
            for document in documents:
                post = Post()
                post._id = ObjectId(document['_id'])
                post.title = document['title']
                post.text = document['text']
                post.creator = create_post_creator(document['creator'])
                post.publish_datetime = document['publish_datetime']
                post.file = document['file']
                post.file_thumbnail = document['file_thumbnail']
                post.container_id = document['group_id']
                post.container_type = 'groups'
                from parsadp.ipn.domain.aggregates.group.model.group import Group as GroupModel
                group = GroupModel.get_by_id(document['group_id'])
                from parsadp.ipn.domain.aggregates.post.model.group import Group
                post.container_info = create_group_from_dict(group)
                post.is_admin_post = str(document['creator']['person_id']) == "5601216789562c13d4567f0a"
                post.users_who_removed_admin_shares = []
                post.like_count = document['like_count'] #len(document['likes'])
                post.comment_count = comment_count(post._id, 'group_posts')
                post.viewer_count = 0
                if document['likes']:
                    create_like_from_post_likes(document['likes'], 'groups', document['group_id'], document['_id'])
                results.append(post)
                print("group_post: ", post._id)
        return results

    def create_post_from_wall_post(documents):
        from parsadp.ipn.domain.aggregates.post.model.post import Post

        results = []
        if documents:
            for document in documents:
                post = Post()
                post._id = ObjectId(document['_id'])
                post.title = document['subject']
                post.text = document['description']
                post.creator = create_post_creator(document['creator'])
                post.publish_datetime = document['created_date']
                post.file = document['file']
                post.file_thumbnail = document['file_thumbnail']
                post.container_id = document['creator']['person_id']
                post.container_type = 'walls'
                post.container_info = None
                post.is_admin_post = str(document['creator']['person_id']) == "5601216789562c13d4567f0a"
                post.users_who_removed_admin_shares = []
                post.like_count = document['like_count'] #len(document['likes'])
                post.comment_count = comment_count(post._id, 'wall_posts')
                post.viewer_count = 0
                create_like_from_post_likes(document['likes'], 'walls', document['creator']['person_id'], document['_id'])
                results.append(post)
                print("wall_post: ", post._id)
        return results

    def create_comment_from_group_post_comment(documents):
        from parsadp.ipn.domain.aggregates.comment.model.comment import Comment

        results = []
        if documents:
            for document in documents:
                comment = Comment()
                comment._id = ObjectId(document['_id'])
                comment.text = document['text']
                comment.creator = create_comment_creator(document['creator'])
                comment.publish_datetime = document['publish_datetime']
                if 'file' in document:
                    comment.file = document['file']
                else:
                    comment.file = None
                if 'file_thumbnail' in document:
                    comment.file_thumbnail = document['file_thumbnail']
                else:
                    comment.file_thumbnail = None
                comment.container_type = 'groups'
                comment.container_id = document['group_id']
                comment.parent_post_id = document['group_post_id']
                comment.parent_first_level_comment_id = None
                comment.parent_type = 'posts'
                comment.like_count = document['like_count']
                comment.comment_count = 0
                create_like_from_post_comment_likes(document['likes'], 'groups', document['group_id'], document['group_post_id'], document['_id'])
                results.append(comment)
                print("group_post_comment: ", comment._id)
        return results


    def create_comment_from_company_post_comment(documents):
        from parsadp.ipn.domain.aggregates.comment.model.comment import Comment

        results = []
        if documents:
            for document in documents:
                comment = Comment()
                comment._id = ObjectId(document['_id'])
                comment.text = document['text']
                comment.creator = create_comment_creator(document['creator'])
                comment.publish_datetime = document['publish_datetime']
                if 'file' in document:
                    comment.file = document['file']
                else:
                    comment.file = None
                if 'file_thumbnail' in document:
                    comment.file_thumbnail = document['file_thumbnail']
                else:
                    comment.file_thumbnail = None
                comment.container_type = 'companies'
                comment.container_id = document['company']['_id']
                comment.parent_post_id = document['company_post_id']
                comment.parent_first_level_comment_id = None
                comment.parent_type = 'posts'
                comment.like_count = document['like_count']
                comment.comment_count = 0
                create_like_from_post_comment_likes(document['likes'], 'companies', document['company']['_id'], document['company_post_id'], document['_id'])
                results.append(comment)
                print("company_post_comment: ", comment._id)
        return results


    def create_comment_from_wall_post_comment(documents):
        from parsadp.ipn.domain.aggregates.comment.model.comment import Comment

        results = []
        if documents:
            for document in documents:
                comment = Comment()
                comment._id = ObjectId(document['_id'])
                comment.text = document['text']
                comment.creator = create_comment_creator(document['creator'])
                comment.publish_datetime = document['publish_datetime']
                if 'file' in document:
                    comment.file = document['file']
                else:
                    comment.file = None
                if 'file_thumbnail' in document:
                    comment.file_thumbnail = document['file_thumbnail']
                else:
                    comment.file_thumbnail = None
                comment.container_type = 'walls'
                comment.container_id = document['creator']['person_id']
                comment.parent_post_id = document['wall_post_id']
                comment.parent_first_level_comment_id = None
                comment.parent_type = 'posts'
                comment.like_count = document['like_count']
                comment.comment_count = 0
                create_like_from_post_comment_likes(document['likes'], 'walls', document['creator']['person_id'], document['wall_post_id'], document['_id'])
                results.append(comment)
                print("wall_post_comment: ", comment._id)
        return results

    def create_like_from_post_likes(likes_list, container_type, container_id, post_id):
        from parsadp.ipn.domain.aggregates.like.model.like import Like

        if likes_list:
            for document in likes_list:
                like = Like()
                like._id = ObjectId()
                like.creator = create_like_creator(document)
                like.created_date = datetime.utcnow().isoformat()
                like.container_type = container_type
                like.container_id = str(container_id)
                # container_info = None
                like.parent_type = 'posts'
                like.parent_post_id = str(post_id)
                like.parent_first_level_comment_id = None
                like.parent_second_level_comment_id = None
                # parent_info = None
                likes.append(like)
                print("{}_post_like: {}".format(container_type, like._id))

    def create_like_from_post_comment_likes(likes_list, container_type, container_id, post_id, comment_id):
        from parsadp.ipn.domain.aggregates.like.model.like import Like

        if likes_list:
            for document in likes_list:
                like = Like()
                like._id = ObjectId()
                like.creator = document
                like.created_date = datetime.utcnow().isoformat()
                like.container_type = container_type
                like.container_id = str(container_id)
                # container_info = None
                like.parent_type = 'posts'
                like.parent_post_id = str(post_id)
                like.parent_first_level_comment_id = str(comment_id)
                like.parent_second_level_comment_id = None
                # parent_info = None
                likes.append(like)
                print("{}_post_comment_like: ".format(container_type), like._id)

    def create_post_creator(creator):
        from parsadp.ipn.domain.aggregates.post.model.creator import Creator
        _creator = None
        if creator:
            _creator = Creator()
            _creator.person_id = creator['person_id']
            _creator.person_name = creator['person_name']
            _creator.person_last_name = creator['person_last_name']
            _creator.person_image = creator['person_image']
            _creator.last_job_company = creator['last_job_company']
            _creator.last_job_title = creator['last_job_title']
        return _creator


    def create_comment_creator(creator):
        from parsadp.ipn.domain.aggregates.comment.model.creator import Creator
        _creator = None
        if creator:
            _creator = Creator()
            _creator.person_id = creator['person_id']
            _creator.person_name = creator['person_name']
            _creator.person_last_name = creator['person_last_name']
            _creator.person_image = creator['person_image']
            _creator.last_job_company = creator['last_job_company']
            _creator.last_job_title = creator['last_job_title']
        return _creator


    def create_like_creator(creator):
        from parsadp.ipn.domain.aggregates.like.model.creator import Creator
        _creator = None
        if creator:
            _creator = Creator()
            _creator.person_id = creator['person_id']
            _creator.person_name = creator['person_name']
            _creator.person_last_name = creator['person_last_name']
            _creator.person_image = creator['person_image']
            _creator.last_job_company = creator['last_job_company']
            _creator.last_job_title = creator['last_job_title']
        return _creator

    def comment_count(post_id, post_type):
        count = 0
        if post_type == 'group_posts':
            count = db.group_post_comment.find({'group_post_id': str(post_id)}).count()
        if post_type == 'company_posts':
            count = db.company_post_comment.find({'company_post_id': str(post_id)}).count()
        if post_type == 'wall_posts':
            count = db.wall_post_comment.find({'wall_post_id': str(post_id)}).count()
        return count

    def create_company_from_dict(company):
        from parsadp.ipn.domain.aggregates.post.model.company import Company

        if company:
            company_detail = Company()
            company_detail._id = company['_id']
            company_detail.name = company['name']
            company_detail.image = company['image']
            company_detail.company_type_id = company['company_type_id']
            company_detail.company_type = company['company_type']
            company_detail.company_size_id = company['company_size_id']
            company_detail.company_size = company['company_size']
            company_detail.company_industry_id = company['company_industry_id']
            company_detail.company_industry = company['company_industry']
            company_detail.company_operation_id = company['company_operation_id']
            company_detail.company_operation = company['company_operation']
            company_detail.is_comment_allowed = company['is_comment_allowed']
            company_detail.is_like_allowed = company['is_like_allowed']
            return company_detail
        return None

    def create_group_from_dict(group_obj):
        from parsadp.ipn.domain.aggregates.post.model.group import Group

        if group_obj:
            group = Group()
            group._id = group_obj._id
            group.title = group_obj.title
            group.description = group_obj.description
            group.logo = group_obj.logo
            group.creator_id = group_obj.creator.person_id
            group.is_channel = group_obj.is_channel
            group.is_private = group_obj.is_private
            group.is_comment_allowed = group_obj.is_comment_allowed
            group.is_like_allowed = group_obj.is_like_allowed
            return group
        return None

    group_posts = db.group_post.find({})
    group_post_comments = db.group_post_comment.find({})
    company_posts = db.company_post.find({})
    company_posts_comments = db.company_post_comment.find({})
    wall_posts = db.wall_post.find({})
    wall_posts_comments = db.wall_post_comment.find({})

    _posts = create_post_from_company_post(company_posts)
    if _posts:
        posts.extend(_posts)

    _posts = create_post_from_group_post(group_posts)
    if _posts:
        posts.extend(_posts)

    _posts = create_post_from_wall_post(wall_posts)
    if _posts:
        posts.extend(_posts)

    _comments = create_comment_from_company_post_comment(company_posts_comments)
    if _comments:
        comments.extend(_comments)

    _comments = create_comment_from_group_post_comment(group_post_comments)
    if _comments:
        comments.extend(_comments)

    _comments = create_comment_from_wall_post_comment(wall_posts_comments)
    if _comments:
        comments.extend(_comments)

    for post in posts:
        # db.post.update({"_id": post["_id"]}, post, upsert=False)
        from parsadp.ipn.domain.aggregates.post.repository.mongo.post_writer import PostWriter

        post_writer = PostWriter()
        post_writer.create(post)
        print(post)
    print("\n\n {} posts_copied".format(str(len(posts))))

    for comment in comments:
        # db.comment.update({"_id": comment["_id"]}, comment, upsert=False)
        from parsadp.ipn.domain.aggregates.comment.repository.mongo.comment_writer import CommentWriter
        comment_writer = CommentWriter()
        comment_writer.create(comment)
        print(comment)
    print("\n\n {} comments_copied".format(str(len(comments))))

    for like in likes:
        # db.post.update({"_id": like["_id"]}, like, upsert=False)
        from parsadp.ipn.domain.aggregates.like.repository.mongo.like_writer import LikeWriter
        like_writer =  LikeWriter()
        like_writer.create(like)
        print(like)
    print("\n\n {} likes_copied".format(str(len(likes))))

create_post_comment_like_from_old_db()



