import React, { useEffect, useState } from "react";

function ReviewList({ placeId }) {
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/places/${placeId}/reviews`)
      .then((resp) => {
        if (!resp.ok) {
          throw new Error("Failed to fetch reviews");
        }
        return resp.json();
      })
      .then((data) => setReviews(data))
      .catch((error) => setError(error.message));
  }, [placeId]);

  // function removePlace(placeId) {
  //   const filteredPlaces = places.filter((place) => place.id !== placeId);
  //   setPlaces(filteredPlaces);
  // }
  // const filteredPlaces = places.filter((place) => {
  //   const lowercaseSearch = search ? search.toLowerCase() : '';
  //   const lowercaseName = place.name ? place.name.toLowerCase() : '';
  //   return lowercaseName.includes(lowercaseSearch);
  // });

  // const placeCards = filteredPlaces.map((place) => (
  //   <PlaceCard key={place.id} place={place} removePlace={removePlace} />
  // ));

  return (
    <div>
      <h3>Reviews</h3>
      {error && <p>Error: {error}</p>}
      {reviews.length === 0 ? (
        <p>No Reviews found.</p>
      ) : (
        <ul>
          {reviews.map((review) => (
            <li key={review.id}>
              <p>{review.content}</p>
              <p>Rating: {review.rating}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ReviewList;
