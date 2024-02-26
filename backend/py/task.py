from dataclasses import dataclass
from collections import Counter, defaultdict

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int


"""
Task 1
"""
def leafFiles(files: list[File]) -> list[str]:
    numChildren = {}
    for f in files:
        if f.id not in numChildren.keys():
            numChildren[f.id] = 0
        if f.parent != -1:
            numChildren[f.parent] = numChildren.get(f.parent, 0) + 1
    
    leaves = []
    for f in files:
        if numChildren[f.id] == 0:
            leaves.append(f.name)
    return leaves


"""
Task 2
"""
def kLargestCategories(files: list[File], k: int) -> list[str]:
    numFiles = Counter()
    for f in files:
        numFiles.update(f.categories)
    
    # sort in descending order of values, then by alphabetical of keys
    sortedCategories = sorted(numFiles.items(), key=lambda f: (-f[1], f[0]))
    return [c for c, _ in sortedCategories[:k]]


"""
Task 3
"""
def largestFileSize(files: list[File]) -> int:
    fileSize = {}
    children = defaultdict(list)
    totalSizes = {}

    def getChildrenSizes(id):
        if id in totalSizes.keys():
            return totalSizes[id]

        totalSizes[id] = fileSize[id]
        if id in children.keys():
            for c in children[id]:
                totalSizes[id] += getChildrenSizes(c)
        return totalSizes[id]
        
    # store list of children for each file and map id to size
    for f in files:
        fileSize[f.id] = f.size
        if f.parent != -1:
            children[f.parent].append(f.id)
    
    # calculate total size for each file
    for f in files:
        totalSizes[f.id] = getChildrenSizes(f.id)
    
    return 0 if not totalSizes else max(totalSizes.values())


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992
