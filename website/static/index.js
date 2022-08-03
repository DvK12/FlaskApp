function deletetransaction(dataTuple) {
  let transactionId = dataTuple[0];
  let month = dataTuple[1];
  fetch("/delete-transaction", {
      method: "POST",
      body: JSON.stringify({ transactionId: transactionId
      }),
    }).then((_res) => {
      window.location.href = "/month/"+month;
    });
  }