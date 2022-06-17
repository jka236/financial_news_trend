import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import React, { useEffect, useState } from "react";
import BarChart from "../components/barChart";

const Submission = ({ words }) => {
  function formatDate(d) {
    var month = "" + (d.getMonth() + 1);
    var day = "" + d.getDate();
    var year = d.getFullYear();

    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;

    return [year, month, day].join("-");
  }

  var weekAgo = new Date(new Date().setDate(new Date().getDate() - 7));
  var current_date = new Date();

  var today = formatDate(current_date);
  var weekAgo = formatDate(weekAgo);

  // get total days between two dates
  var days = Math.floor(current_date / 86400000);

  return (
    <>
      <main>
        <Container maxWidth="sm">
          <Box sx={{ my: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Top 10 Most Frequent Keywords From Last 7 Days
            </Typography>
            <Typography variant="h5" component="h1" gutterBottom>
              From {today} To {weekAgo}
            </Typography>

            <BarChart
              width={640}
              height={400}
              data={words.data[0]}
              fromDate={days - 7}
              toDate={days}
            />
          </Box>
          {/* <DatePicker label={"From Date"} />
          <DatePicker label={"To Date"} /> */}
        </Container>
      </main>
    </>
  );
};

export async function getServerSideProps() {
  const res = await fetch("http://127.0.0.1:8000/noun");
  const words = await res.json();

  return {
    props: {
      words,
    },
  };
}

export default Submission;
