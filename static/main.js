async function getVersions(type) {
    try {
        const response = await fetch(`/versions/${type}`);
        const data = await response.json();
        return data
    } 
    
    catch (error) {
        console.error('Error:', error);
        return []
    }
}

const mainBtn = document.getElementById('main-btn');

const minecraftToLaunch = document.getElementById('version-to-launch');

getVersions('installed').then(installedVersions => {
    let [version, modification] = minecraftToLaunch.textContent.split(' ')
    
    if (!!modification) {
        if (version in installedVersions[modification]) {
            minecraftToLaunch.style.color = 'white'
        }
    }

    else {
        if (installedVersions['vanilla'].includes(version)) {
            minecraftToLaunch.style.color = 'white'
        }
    }

    if (minecraftToLaunch.style.color === 'white') {
            mainBtn.textContent = 'Play'
            mainBtn.name = 'play'
        }

    else {
        mainBtn.textContent = 'Install'
        mainBtn.name = 'install'
    }
})

const modificationsList = document.getElementById('modifications-list');

minecraftToLaunch.addEventListener('click', () => {
    minecraftToLaunch.style.display = 'none'
    mainBtn.style.display = 'none'
    modificationsList.style.display = 'flex'
});

const versionsList = document.getElementById('versions-list');

const scrollSpeed = 30;

versionsList.addEventListener('wheel', (event) => {
    event.preventDefault();
    const direction = event.deltaY > 0 ? 1 : -1;
    versionsList.scrollLeft += direction * scrollSpeed;
});

let scrollInterval

const backwardBtn = document.getElementById('backward-btn');

backwardBtn.addEventListener('mousedown', () => {
    scrollInterval = setInterval(() => {
        versionsList.scrollLeft -= scrollSpeed;
    }, 5);
});

backwardBtn.addEventListener('mouseup', () => {
    clearInterval(scrollInterval)
});

const forwardBtn = document.getElementById('forward-btn');

forwardBtn.addEventListener('mousedown', () => {
    scrollInterval = setInterval(() => {
        versionsList.scrollLeft += scrollSpeed;
    }, 5);
});

forwardBtn.addEventListener('mouseup', () => {
    clearInterval(scrollInterval)
});

const backwardImg = document.querySelector('#backward-btn img');
const forwardImg = document.querySelector('#forward-btn img');

const main = document.querySelector('main')

$(document).on('click', '.modification', function() {
    modification = $(this).val()
     
    getVersions(modification).then(versions => {
        getVersions('installed').then(installedVersions => {
            for (let i = 0; i <= versions.length; i++) {
                let button = document.createElement("button")

                button.className = 'versions-list-btn'
                button.textContent = versions[i]
                
                if (modification === 'vanilla') {
                    if (installedVersions['vanilla'].includes(versions[i])) {
                        button.style.color = 'white'
                    }
                }

                else {
                    if (versions[i] in installedVersions[modification]) {
                        button.style.color = 'white'
                    }
                }

                versionsList.appendChild(button)
            }
        })
    })
    modificationsList.style.display = 'none'
    minecraftToLaunch.style.display = 'none'
    mainBtn.style.display = 'none'

    versionsList.style.display = 'flex'   
    backwardBtn.style.display = 'block'
    forwardBtn.style.display = 'block'
    main.style.display = 'flex'
});

$(document).on('click', '.versions-list-btn', function() {
    fetch('/update_minecraft_to_launch', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({ version: $(this).text(), modification: modification === 'vanilla' ? null : modification })
    })
    .then(response => response.json())
    .catch(error => {
        console.error(error)
    })
    backwardImg.style.display = 'none'
    forwardImg.style.display = 'none'
    versionsList.style.display = 'none'
    minecraftToLaunch.style.display = 'block'
});