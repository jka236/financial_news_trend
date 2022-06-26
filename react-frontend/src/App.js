import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import React, { useEffect, useState } from "react";
import TrendChart from "./components/trendChart";
import axios from "axios";
import { CircularProgress } from "@mui/material";

function App() {
  const [words, setWords] = useState();
  const [loading, setLoading] = useState(true);

  function formatDate(d) {
    var month = "" + (d.getMonth() + 1);
    var day = "" + d.getDate();
    var year = d.getFullYear();

    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;

    return [year, month, day].join("-");
  }

  var weekAgo = new Date(new Date().setDate(new Date().getDate() - 6));
  var current_date = new Date();

  var today = formatDate(current_date);
  weekAgo = formatDate(weekAgo);

  // get total days between two dates
  var days = Math.floor(current_date / 86400000);
  // var days = 19155;

  useEffect(() => {
    axios
      .get("https://news-trend-tracking.herokuapp.com/noun")
      // .get("http://localhost:8000/noun")
      .then((res) => {
        setLoading(false);
        setWords(res.data.data[0]);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <React.Fragment>
      <>
        <main>
          <Container maxWidth="sm">
            <Box sx={{ my: 4 }}>
              <Typography variant="h4" component="h1" gutterBottom>
                Top 10 Most Frequent Keywords From Last 7 Days
              </Typography>
              <Typography variant="h5" component="h1" gutterBottom>
                From {weekAgo} To {today}
              </Typography>
              {loading && (
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    marginTop: "50px",
                  }}
                >
                  <CircularProgress />
                </div>
              )}
              {!loading && (
                <TrendChart
                  width={640}
                  height={400}
                  data={words}
                  fromDate={days - 7}
                  toDate={days}
                />
              )}
            </Box>
          </Container>
        </main>
      </>
    </React.Fragment>
  );
}

export default App;
