#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', name='fk_oauth_grant_user'))
#
# user = db.relationship('User', single_parent=True, cascade='all,delete,delete-orphan')
#
#     db.Column('label_id', db.BigInteger, db.ForeignKey('labels.id', ondelete='CASCADE'), nullable=False),
#
#     db.Column('mention_id', db.BigInteger, db.ForeignKey('mentions.id', ondelete='CASCADE'), nullable=False),
#     ForeignKeyConstraint(['mention_id'], ['mentions.id'], ondelete='CASCADE', name='fk_relation_label_mention_mention'),
#     ForeignKeyConstraint(['label_id'], ['labels.id'], ondelete='CASCADE', name='fk_relation_label_mention_label'),
#
#     memberships = db.relationship('Membership', back_populates='user', cascade="all,delete,delete-orphan",
#
#                                  passive_deletes=True)