<template>
    <nav class="navbar navbar-tiktech navbar-expand-lg">
        <a class="navbar-brand" href="/">
            <img src="../assets/logo.png" class="d-inline-block align-top" width="30" height="30" alt="TikTech"> Tickets
        </a>
        <ul class="navbar-nav mr-auto">
            <li :class="'nav-item ' + (active == 'my-tickets' ? 'active' : '')">
                <a class="nav-link" href="/user/123123123">My active Tickets <span class="sr-only">(current)</span></a>
            </li>
            <li :class="'nav-item ' + (active == 'submit-ticket' ? 'active' : '')">
                <a class="nav-link" href="/form">Submit a ticket</a>
            </li>
            <li :class="'nav-item ' + (active == 'archive' ? 'active' : '')">
                <a class="nav-link" href="#">Archive</a>
            </li>
            <li :class="'nav-item ' + (active == 'course' ? 'active' : '')">
                <a class="nav-link" href="/courses">Course overview</a>
            </li>
        </ul>
    </nav>
</template>

<script>

  export default {
      props: ['active'],
      data: function () {
          return {};
      }
  }

</script>
