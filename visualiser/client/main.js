import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

import './main.html';




Template.graphVis.helpers({
    'dataset': function() {
        return "PyGraphistry%2FHJ6TYL0OVO";
    }
});

Template.sidebar.events({
    'click #graph-choice' (event, instance) {
        console.log(event.currentTarget.getAttribute('dataset'))
    },
});

Template.sidebar.helpers({
    'current_dataset': function() {
        return {
            'name': "Gen Capacities",
            'id': "PyGraphistry%2FHJ6TYL0OVO",
            'description': "This dataset is a weighted graph of the Australian transmission network. Generators have been added to their nearest line interconnection point by Vincenty distance. Generator types are indicated by node colors. generator capacities are indicated by node sizes. Scroll-wheel up/down to zoom, mouse over nodes or edges for more information."
        };
    }
})