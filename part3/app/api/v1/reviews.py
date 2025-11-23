from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        if isinstance(current_user, dict):
            user_id = current_user.get('id')

        else:
            user_id = current_user 

        try:
            data = request.get_json()
            data['user_id'] = user_id
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error' : f"Unexpected error: {str(e)}"}, 400
        
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = []
        for r in facade.get_all_reviews():
            reviews.append(r.to_dict())
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': f"The review with ID {review_id} does not exist"}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {'error': f"The review with ID {review_id} does not exist"}, 404
        
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        data = request.get_json()
        try:
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'error': f"The review with ID {review_id} does not exist"}, 404
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"Unexpected error: {str(e)}"}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {'error': f"The review with ID {review_id} does not exist"}, 404
        
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}
        
        facade.delete_review(review_id) 
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = [r.to_dict() for r in facade.get_reviews_by_place(place_id)]
            return reviews, 200
        except ValueError as e: 
            return {'error': str(e)}, 404
