class FileUtils:
    def formatFileSize(sizeBytes):
        sizeBytes = float(sizeBytes)
        result = float(abs(sizeBytes))
        suffix = "B"
        if result > 1024:
            suffix = "KB"
            result = result / 1024

        if result > 1024:
            suffix = "MB"
            result = result / 1024

        if result > 1024:
            suffix = "GB"
            result = result / 1024

        if result > 1024:
            suffix = "TB"
            result = result / 1024

        if result > 1024:
            suffix = "PB"
            result = result / 1024
        return format(result, ".2f") + suffix


