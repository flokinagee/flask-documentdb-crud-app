from flask_table import Table, Col, LinkCol
 
class Results(Table):
    _id = Col('CustId')
    name = Col('Name')
    email = Col('Email')
    amount = Col('Amount')
    month = Col('Month')
    charm = Col('Lucky Charm')
    ballot = LinkCol('Ballot', 'run_ballot', url_kwargs=dict(id='_id'))
    edit = LinkCol('Update', 'edit_view', url_kwargs=dict(id='_id'))
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='_id'))

# from flask_table import Table, Col, LinkCol
 
# class Results(Table):
#     _id = Col('CustId')
#     name = Col('Name')
#     surname = Col('Surname')
#     email = Col('Email')
#     edit = LinkCol('Update', 'edit_view', url_kwargs=dict(id='_id'))
#     delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='_id'))