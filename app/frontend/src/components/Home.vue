<template>
	<div id="page-top">

		<!-- Header -->
		<header class="masthead">
			<div class="container">
				<div class="intro-text">
					<img class="logo-main" src="../assets/ProjectSoftwareTIKTECHBlack.png" alt="logo">
					<div class="intro-lead-in">Welcome to a brand new way of communication!</div>
					<div class="intro-heading text-uppercase">Let us introduce you to TikTech</div>
					<!-- <a href="#" v-scroll-to="'#services'" class="btn btn-primary btn-xl text-uppercase js-scroll-trigger scoll-button" >Find out more!</a> -->
					<a href="#" v-scroll-to="'#messaging-structure'" class="text-uppercase button scroll-button btn-arrow">
						<span>Find out more!
							<svg width="40" height="20" viewBox="-2.5 -5 75 60" preserveAspectRatio="none">
								<path d="M0,0 l35,50 l35,-50" fill="none" stroke="white" stroke-linecap="round" stroke-width="5" />
							</svg>
							<svg width="40" height="20" viewBox="-2.5 -5 75 60" preserveAspectRatio="none">
								<path d="M0,-20 l35,50 l35,-50" fill="none" stroke="white" stroke-linecap="round" stroke-width="5" />
							</svg>
						</span>
					</a>
				</div>
			</div>
		</header>

		<!-- The Messaging Structure -->
		<section id="messaging-structure" class="message-struct-section">
			<div class="container">
				<div class="row">
					<div class="col-lg-12 text-center">
						<h2 class="section-heading text-uppercase">The Messaging Structure</h2>
						<div class="subheading-middle">
							<h3 class="section-subheading text-muted" style="left: 50%; width: 50%;color: #3e4042 !important;">"TIKTECH has everything you need for a smooth academic career! With our advanced ticket service, the problems of communication
								between students and supervisors are ancient history. With slick interfaces and intuitive design, creating the right
								channels between the right people has never been easier." - TIKTECH CEO</h3>
						</div>
					</div>
				</div>
				<div class="row text-center">
					<div class="col-md-6">
						<h4 class="service-heading">The Student</h4>
						<p class="p-subtext">As enrolled student, you can message your supervisors through the web interface or through the existing mail channels.
							You will never have to wait long on a reply again as either message will be directed to the right person. You may
							view your conversations with supervisors and reply in a convenient way.</p>
					</div>
					<div class="col-md-6">
						<h4 class="service-heading">The Supervisor</h4>
						<p class="p-subtext">As Supervisor, you can see which tickets have been assigned to you! You may also choose to view all tickets in a course,
							discuss tickets with your colleagues and have them join you in answering those harder questions. Create labels and
							assign yourselfs to them to direct questions to the right people. Set up your courses e-mail to intergrate into TIKTECH
							seamlessly! The possibilities are endless.</p>
					</div>
				</div>
				<div class="middle-display">
					<a href="#" v-scroll-to="'#services'" class="button text-uppercase scroll-button btn-arrow">
						<span>Our Services!
							<svg width="40" height="20" viewBox="-2.5 -5 75 60" preserveAspectRatio="none">
								<path d="M0,0 l35,50 l35,-50" fill="none" stroke="white" stroke-linecap="round" stroke-width="5" />
							</svg>
							<svg width="40" height="20" viewBox="-2.5 -5 75 60" preserveAspectRatio="none">
								<path d="M0,-20 l35,50 l35,-50" fill="none" stroke="white" stroke-linecap="round" stroke-width="5" />
							</svg>
						</span>
					</a>
				</div>
			</div>
		</section>

		<!-- Services -->
		<section id="services" class="service-section">
			<div class="container">
				<div class="row">
					<div class="col-lg-12 text-center">
						<h2 class="section-heading text-uppercase">Services</h2>
					</div>
				</div>
				<div class="row text-center">
					<div class="col-md-4">
						<h4 class="service-heading">Ticketing system</h4>
						<p class="text-muted">The answer to an unclear, messy, shared mail server? TIKTECH's organized ticketing system! Sent mails will be converted
							to tickets and processed accordingly, but every reply you send will magically end up in the student's inbox as well!</p>
					</div>
					<div class="col-md-4">
						<h4 class="service-heading">Labeling conversations</h4>
						<p class="text-muted">Sort your tickets based on their content. Is the question based on a certain assignment? Label it! Is it a personal
							issue? Label it! No idea what the student is trying to convey? Label everything accordingly and help everyone keep
							the overview.</p>
					</div>
					<div class="col-md-4">
						<h4 class="service-heading">Integration and security</h4>
						<p class="text-muted">Make sure no senior students or others with malicious intent can troll the hard-working TAs with our secure authorization.
							TIKTECH is safe and accesible only to those students enrolled in the course. </p>
					</div>
					<div class="col-md-12">
						<h6 class="sevice-subheading">Check out the people who made this possible:</h6>
						<br />
						<br />
						<router-link to="/team" class="team-button">Meet the team!
						</router-link>
					</div>
				</div>
				<div class="middle-display">
					<router-link to="/login" :class="'button text-uppercase scroll-button btn-arrow'">
						<span>Get Started Now!
							<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
							 viewBox="0 0 36.1 25.8" enable-background="new 0 0 36.1 25.8" xml:space="preserve">
								<g>
									<line fill="none" stroke="#FFFFFF" stroke-width="3" stroke-miterlimit="10" x1="0" y1="12.9" x2="34" y2="12.9"></line>
									<polyline fill="none" stroke="#FFFFFF" stroke-width="3" stroke-miterlimit="10" points="22.2,1.1 34,12.9 22.2,24.7">
									</polyline>
								</g>
							</svg>
						</span>
					</router-link>
				</div>
			</div>
		</section>
	</div>
</template>

<script>

</script>
