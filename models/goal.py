from flask import flash
from flask_login import current_user
from models.base import BaseModel
from utils.exts import db


class Goal(BaseModel, db.Model):
    amount = db.Column(db.Integer)
    type = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def set_goal(goal_amount, goal_type):
        existing_goal = current_user.goal
        if goal_amount:
            try:
                goal_amount = int(goal_amount)
                if existing_goal:
                    existing_goal.amount = goal_amount
                    existing_goal.type = goal_type
                else:
                    new_goal = {
                        'user_id': current_user.id,
                        'amount': goal_amount,
                        'type': goal_type
                    }
                    current_user.goal = Goal.create(**new_goal)
                flash('Yearly reading goal set successfully!', 'success')
            except ValueError as e:
                flash(f'{e}: Please enter a valid number for the goal.', 'error')
            except Exception as e:
                flash(f'{e}', 'error')
        else:
            flash('Please enter a valid number for the goal.', 'error')
