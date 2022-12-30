from PIL import Image
import os

def combine2Pdf( folderPath, pdfFilePath ):
    files = os.listdir( folderPath )
    jpgFiles = []
    sources = []
    for file in files:
        if 'jpg' in file:
            jpgFiles.append( folderPath + file )
    jpgFiles.sort()
    output = Image.open( jpgFiles[0] )
    jpgFiles.pop( 0 )
    for file in jpgFiles:
        pngFile = Image.open( file )
        if pngFile.mode == "RGB":
            pngFile = pngFile.convert( "RGB" )
        sources.append( pngFile )
    output.save( pdfFilePath, "pdf", save_all=True, append_images=sources )

if __name__ == "__main__":
    folder = "image/"
    pdfFile = "01.pdf"
    combine2Pdf( folder, pdfFile )