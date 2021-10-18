const emailField = document.querySelector("#email");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const otpFeedBackArea = document.querySelector(".otpFeedBackArea");
const verifyOTPFeedback = document.querySelector(".OTPFeedBackArea");
const sendOtpBtn = document.querySelector("#sendOtpBtn");
const verifyOtpBtn = document.querySelector("#verifyOtpBtn");
const changePasswordBtn = document.querySelector("#changePasswordBtn");

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/validate/email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          sendOtpBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class='alert alert-danger'>${data.email_error}</p>`;
        } else {
          sendOtpBtn.removeAttribute("disabled");
        }
      });
  }
});

function sendOTP() {
  sendOtpBtn.innerHTML =
    '<div class="spinner-border text-dark" role="status"><span class="sr-only">Loading...</span></div>';
  let email = $("#email").val();
  $.ajax({
    url: "/validate/send-otp",
    type: "GET",
    data: {
      email: email,
    },
    success: function (data) {
      sendOtpBtn.innerHTML = "Send OTP";
      if (data.otp_error) {
        otpFeedBackArea.style.display = "block";
        otpFeedBackArea.innerHTML = `<p class='alert alert-danger'>${data.otp_error}</p>`;
      } else if(data.otp_sent) {
        otpFeedBackArea.style.display = "block";
        otpFeedBackArea.innerHTML = `<p class='alert alert-success'>${data.otp_sent}</p>`;
        $("#sendOtpBtn").hide();
        $("#afterOTP").slideDown(1000);
      }
    },
  });
}


function verifyOTP() {
  let otp = $("#otp").val();
  let email = $("#email").val();
  $.ajax({
    url: "/validate/verify-otp",
    type: "GET",
    data: {
      email: email,
      otp: otp,
    },
    success: function (data) {
      if (data.otp_mismatch) {
        verifyOTPFeedback.style.display = "block";
        verifyOTPFeedback.innerHTML = `<p class='alert alert-danger'>${data.otp_mismatch}</p>`;
      } else {
        verifyOtpBtn.removeAttribute("disabled");
        otpFeedBackArea.style.display = "none";
        $("#afterOTP").hide();
        $("#newPassword").fadeIn(1000);
      }
    },
  });
}