<!-- Team.vue shows the amazing team of TIKTECH and their roles. -->
<template>
    <div>
        <!-- Teampage -->
        <section id="team" style="padding:50px !important;">
            <div class="col-12 text-center">
                <h3 class="section-heading text-uppercase">The people behind TIKTECH:</h3>
                <hr>

            </div>
            <div class="row text-center">
                <div class="col-md-4">
                    <h4 class="service-heading">Stephan</h4>
                    <p class="text-muted">Mailing systems and parsing</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Jarno</h4>
                    <p class="text-muted">Git master and testing supervisor</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Ravi</h4>
                    <p class="text-muted">Label technology development</p>
                </div>
            </div>
            <div class="row text-center">
                <div class="col-md-4">
                    <h4 class="service-heading">Rens</h4>
                    <p class="text-muted">Ticket creation and backend developer</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Damian</h4>
                    <p class="text-muted">Server manager and backend developer</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Donald</h4>
                    <p class="text-muted">Front/Backend developer</p>
                </div>
            </div>
            <div class="row text-center">
                <div class="col-md-4">
                    <h4 class="service-heading">Hazin</h4>
                    <p class="text-muted">Layout management and frontend developer</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Mitch</h4>
                    <p class="text-muted">Makes homepages great again</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Andrea</h4>
                    <p class="text-muted">Gender diversity administrator and grammar lover</p>
                </div>
            </div>
            <div class="row text-center">
                <div class="col-md-4">
                    <h4 class="service-heading">Matej</h4>
                    <p class="text-muted">Authentication and security</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Pieter</h4>
                    <p class="text-muted">Provincial diversity administrator and frontend/backend developer</p>
                </div>
                <div class="col-md-4">
                    <h4 class="service-heading">Tom</h4>
                    <p class="text-muted">Front/Backend development</p>
                </div>
            </div>
            <div class="middle-display">
                <router-link to="/" :class="'text-uppercase scroll-button btn-arrow'">
                    <span>Back to home
                        <svg version="1.1" id="Layer_2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                            viewBox="-1 0 36.1 27.8" enable-background="new 0 0 36.1 25.8" xml:space="preserve">
                            <g>
                                <line fill="none" stroke="#FFFFFF" stroke-width="3" stroke-miterlimit="10" x1="0" y1="12.9" x2="34" y2="12.9">
                                </line>
                                <polyline fill="none" stroke="#FFFFFF" stroke-width="3" stroke-miterlimit="10" points="12.2, 0 1.3, 12.9 12.2, 24.7">
                                </polyline>
                            </g>
                        </svg>
                    </span>
                </router-link>
            </div>
        </section>
    </div>
</template>