import axios from 'axios'

export const getList = () => {
    return axios
        .get('http://localhost:5000/api/tasks', {
            headers: { 'Content-type': 'application/json' }
        })
        .then(res => {
            var data = []
            Object.keys(res.data).forEach(function (key) {
                var val = res.data[key]
                data.push([val.title, val._id])
            })

            return data
        })
}

export const addToList = term => {
    return axios
        .post(
            'http://localhost:5000/api/task',
            {
                title: term
            },
            {
                headers: { 'Content-type': 'application/json' }
            }
        )
        .then((response) => {
            console.log(response)
        })
}

export const deleteItem = term => {
    axios
        .delete(`http://localhost:5000/api/task/${term}`, {
            headers: { 'Content-type': 'application/json' }
        })
        .then((response) => {
            console.log(response)
        })
        .catch((response) => {
            console.log(response)
        })
}

export const updateItem = (term, id) => {
    return axios
        .put(`http://localhost:5000/api/task/${id}`, {
            title: term
        }, {
                headers: { 'Content-type': 'application/json' }
            }
        )
        .then((response) => {
            console.log(response)
        })
}