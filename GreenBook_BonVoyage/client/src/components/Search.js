import React, { useState } from "react";
import PlaceList from "./PlaceList";

function Search({ onSearch }) {
  const [searchPlace, setSearchPlace] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    onSearch(searchShow);
    setSearchPlace("");
  }
  function handleSearch(event) {
    setSearch(event.target.value);
  }

  return (
    <div className="App">
      <input
        type="text"
        placeholder="Search places"
        value={search}
        onChange={handleSearch}
      />
      <PlaceList search={search} />
    </div>
  );
}

export default Search;
