<template>
    <div>
    	<h1> Ticket sorting</h1>
    	<h1> Proof of concept </h1>

    	<!-- DROPDOWN MENU -->
    	<select v-model="sorting_criteria">
                <option> title </option>
                <option> status </option>
                <option> course </option>
                <option> date </option>
            </select>

    	<!-- TICKET TABLE -->
    	<table>
    		<thead>
    			<tr>
    				<th> Title </th>
    				<th> Status </th>
    				<th> Course </th>
    				<th> Date </th>
    			</tr>
    		</thead>
    		<tbody>
    			<tr v-for="ticket in sorted_tickets">
    				<td> {{ticket.title}} </td>
    				<td> {{ticket.status}} </td>
    				<td> {{ticket.course}} </td>
    				<td> {{ticket.date}} </td>
    			</tr>
    		</tbody>
    	</table>
    </div>
</template>


<script>
    import axios from 'axios'

    export default {
    	data() {
    		return {
    			sorting_criteria: "date",

    			// DUMMY DATA
    			tickets: [{
    					title: 'Question assignment 1',
    					status: 'Answered',
    					course: 'Programming 1',
    					date: '06/08/18'
    				},
    				{
    					title: 'Question assignment 2',
    					status: 'Pending',
    					course: 'Programming 1',
    					date: '06/09/18'
    				},
    				{
    					title: 'Question assignment 1',
    					status: 'Assigned',
    					course: 'Programming 1',
    					date: '03/08/18'
    				},
    				{
    					title: 'Question assignment 1',
    					status: 'Unassigned',
    					course: 'Programming 2',
    					date: '04/05/18'
    				}
    			]
    		}
    	},

    	computed: {
    		sorted_tickets: function() {
    			return this.tickets.sort((a, b) => a[this.sorting_criteria] > b[this.sorting_criteria])
    		}
    	}
    }
</script>
