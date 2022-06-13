import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Link from "../src/Link";
import React, { useEffect, useState } from "react";
import BarChart from "../components/barChart";
import DatePicker from "../components/datePicker";

const Submission = ({ words }) => {
  var current_date = new Date();

  // get total days between two dates
  var days = Math.floor(current_date / 86400000);

  return (
    <>
      <main>
        <Container maxWidth="sm">
          <Box sx={{ my: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Top 5 Most Frequent Keyword From Last 7 Days
            </Typography>
            <BarChart
              width={640}
              height={400}
              data={words.data[0]}
              fromDate={days-7}
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
  const res = await fetch("http://127.0.0.1:8000/word");
  const words = await res.json();

  return {
    props: {
      words,
    },
  };
}

export default Submission;
