const searchbtn = document.querySelector('#search');
const searchbar = document.querySelector('#searchText');

function copy(link) {
    navigator.clipboard.writeText(`https://fastnotes-1-q5784757.deta.app${link}`);
    alert("Link copied to clipboard");
}

searchbtn.addEventListener('click', (e) => {
    e.preventDefault();
    // console.log("search button clicked", "Taking you to google");
    let text = searchbar.value;
    alert(`Searching for ${text} on google`);
    // alert(text);
    window.location.href = `https://www.google.com/search?q=${text}`;
});

