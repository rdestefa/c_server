/* utils.c: server utilities */

#include "server.h"

#include <ctype.h>
#include <errno.h>
#include <string.h>

#include <sys/stat.h>
#include <unistd.h>

/**
 * Determine mime-type from file extension.
 *
 * @param   path        Path to file.
 * @return  An allocated string containing the mime-type of the specified file.
 *
 * This function first finds the file's extension and then scans the contents
 * of the MimeTypesPath file to determine which mimetype the file has.
 *
 * The MimeTypesPath file (typically /etc/mime.types) consists of rules in the
 * following format:
 *
 *  <MIMETYPE>      <EXT1> <EXT2> ...
 *
 * This function simply checks the file extension version each extension for
 * each mimetype and returns the mimetype on the first match.
 *
 * If no extension exists or no matching mimetype is found, then return
 * DefaultMimeType.
 *
 * This function returns an allocated string that must be free'd.
 **/

char * determine_mimetype(const char *path) {
    char *ext;
    char *mimetype;
    char *token;
    char buffer[BUFSIZ];
    FILE *fs = NULL;

    /* Find file extension */
    ext = strrchr(path, '.');

    if (!ext) {
        return strdup(DefaultMimeType);
    } else {
        ext++;
    }

    /* Open MimeTypesPath file */
    fs = fopen(MimeTypesPath, "r");

    /* Check for failure */
    if (!fs) {
        debug("Unable to fopen: %s", strerror(errno));
        fclose(fs);
        return NULL;
    }

    /* Scan file for matching file extensions */
    while (fgets(buffer, BUFSIZ, fs)) {
        mimetype = strtok(skip_whitespace(buffer), WHITESPACE);
        token    = strtok(NULL, WHITESPACE);
        while (token) {
            if (streq(token, ext)) {
                if (fs) fclose(fs);
                return strdup(mimetype);
            }

            token = strtok(NULL, WHITESPACE);
        }
    }

    fclose(fs);
    return strdup(DefaultMimeType);
}

/**
 * Determine actual filesystem path based on RootPath and URI.
 *
 * @param   uri         Resource path of URI.
 * @return  An allocated string containing the full path of the resource on the
 * local filesystem.
 *
 * This function uses realpath(3) to generate the realpath of the
 * file requested in the URI.
 *
 * As a security check, if the real path does not begin with the RootPath, then
 * return NULL.
 *
 * Otherwise, return a newly allocated string containing the real path.  This
 * string must later be free'd.
 **/
char * determine_request_path(const char *uri) {
    char real_path[BUFSIZ];
    char buffer   [BUFSIZ];

    log("Determining request path");

    if (sprintf(real_path, "%s%s", RootPath, uri)) {
        realpath(real_path, buffer);
    }

    if (strncmp(real_path, RootPath, strlen(RootPath))) {
        debug("Real path does not begin with %s", RootPath);
        return NULL;
    } else {
        return strdup(real_path);
    }

    return NULL;
}

/**
 * Return static string corresponding to HTTP Status code.
 *
 * @param   status      HTTP Status.
 * @return  Corresponding HTTP Status string (or NULL if not present).
 *
 * http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
 **/
const char * http_status_string(Status status) {
    static char *StatusStrings[] = {
        "200 OK",
        "400 Bad Request",
        "404 Not Found",
        "500 Internal Server Error",
        "418 I'm A Teapot",
    };

    return StatusStrings[status];
}

/**
 * Advance string pointer pass all nonwhitespace characters
 *
 * @param   s           String.
 * @return  Point to first whitespace character in s.
 **/
char * skip_nonwhitespace(char *s) {
    if (!isspace(*s)) while (!isspace(*s)) s++;

    return s;
}

/**
 * Advance string pointer pass all whitespace characters
 *
 * @param   s           String.
 * @return  Point to first non-whitespace character in s.
 **/
char * skip_whitespace(char *s) {
    if (isspace(*s)) while (isspace(*s)) s++;

    return s;
}

/* vim: set expandtab sts=4 sw=4 ts=8 ft=c: */
