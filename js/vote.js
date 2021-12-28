function populate_voting_list() {
  var list = document.querySelector('.gallery');
  [...list.children]
    .forEach(movie=>votes[movie.id] = 0);
  console.log(votes)
}

function disqualify(movie) {
  delete votes[movie.id]
  console.log(votes)
  movie.remove()
}

function good(movie) {
  console.log(movie.id)
  votes[movie.id] = votes[movie.id]+1;
  console.log(votes)
  redraw(votes)
}

function bad(movie) {
  console.log(movie.id)
  votes[movie.id] = votes[movie.id]-1;
  console.log(votes)
  redraw(votes)
}

function redraw() {
  var list = document.querySelector('.gallery');
  [...list.children]
    .sort((a,b)=>votes[a.id]<votes[b.id])
    .forEach(movie=>list.appendChild(movie));
}

function output_result() {
  document.getElementById("result").innerHTML = JSON.stringify(votes);
}
