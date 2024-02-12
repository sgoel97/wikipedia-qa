import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [response, setReponse] = useState("");

  const onSubmit = () => {
    axios
      .get(`http://localhost:8000/api/v1/question/`, {
        params: { q: query },
      })
      .then((res) => {
        const queryResponse = res.data;
        console.log(res);
        setReponse(queryResponse);
      });
  };

  return (
    <div
      style={{
        width: "100vw",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <h1>Wikipedia Q and A</h1>
      <br />
      <textarea
        placeholder="enter query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows="4"
        style={{ width: "50vw" }}
      />
      <br />
      <button onClick={onSubmit}>Search</button>
      <br />
      <p>{response}</p>
    </div>
  );
}

export default App;
