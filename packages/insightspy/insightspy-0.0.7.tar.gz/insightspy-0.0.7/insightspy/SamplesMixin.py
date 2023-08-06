from insightspy.SessionCore import RequestCore
from insightspy.utils import _list_to_int_list, _download
import pandas as pd
import os


class SamplesMixin(RequestCore):
    """Samples PortalSession mixin

    Mixin for the PortalSession class which contains methods for sample related
    routes.
    """

    def samples(self, tag_suffix="_tag_dupl", sample_ids=None):
        """List samples

        Lists samples accessible withthin the current portal session. Sample access is
        limited by user id and the current session project if one is set.

        Args:
            tag_suffix (str):  the suffix that is appended to the column name if a tag
                shares the same name as one of the columns in the core database used to
                describe the samples
            sample_ids (int, [int]):  one or more sample ids to filter on (optional).
                This will also override any filtering from the project scope.

        Examples:
            >>> # p is a logged in portal session
            >>> p.samples()
            >>> # To only retrieve metadata about specific samples
            >>> p.samples(sample_ids = [32, 35, 42])

        Returns:
            DataFrame: table of sample metadata
        """
        if sample_ids is not None:
            ignore_project = True
            if not isinstance(sample_ids, list):
                sample_ids = [sample_ids]
            sample_ids = _list_to_int_list(sample_ids)
        else:
            ignore_project = False
        # List keys to export to user
        export_keys = [
            "sample_id",
            "description",
            "sample_type",
            "reference_genome",
            "revision_id",
            "tags",
        ]
        out = [
            {key: v[key] for key in export_keys}
            for v in self._post(
                "sample/retrieve",
                {
                    "tagsAsDict": True,
                    "sample_ids": sample_ids,
                    "ignoreProject": ignore_project,
                },
                expect_data=True,
            )["response"]["data"]
        ]
        out = pd.DataFrame.from_dict(out)
        if "tags" in out:
            out = out.join(
                pd.DataFrame(out.pop("tags").values.tolist()), rsuffix=tag_suffix
            )
        return out

    def gene_tpm(self, sample_ids):
        """Get gene TPMs

        Get transcripts per million (TPMs) values for all pre-quantified genes in a
            sample

        Args:
            sample_ids (int, [int]):  one or more sample ids

        Examples:
            >>> # p is a logged in portal session
            >>> p.gene_tpm([33, 48])

        Returns:
            DataFrame:
                table of gene TPMs with sample ids as column names and gene names as row
                names
        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        counts = self._post(
            "sample/TPM",
            {
                "sample_ids": sample_ids,
                "minimal": True,
                "raw_counts": False,
                "pseudocounts": 0,
            },
            expect_data=True,
        )["response"]["data"]
        out = pd.DataFrame.from_dict(counts[0], orient="index").sort_index()
        out.columns = [str(x["sample_id"]) for x in counts[1]]
        return out

    def submit_annotation_count(self, annotation_id, sample_ids):
        """Submit an annotation count job

        For a given annotation set and a given set of sample_ids, count
        up the number of reads over those samples.

        Args:
            annotation_id (int): the id from the database
            sample_ids (int, list): a list of sample_ids from the database
        Returns:
            None:
                Just a print statement saying that it has been successfully submitted
        """
        response = self._post(
            "sample/annotation",
            {
                "annotation_id": annotation_id,
                "sample_ids": sample_ids,
                "retrieve": False,
            },
            expect_data=False,
        )["response"]
        if response["notification"]:
            print(response["notification"])
        return response

    def get_annotation_count(self, annotation_id, sample_ids):
        """Retrieve the annotation count data

        For a given annotation set and a given set of sample_ids, retrieve
        the underlying count data for each of those intervals across those samples.
        Note that this will only return if all the samples within the get method
        have been submitted and that job has successfully been run.

        Args:
            annotation_id (int): the id from the database
            sample_ids (int, list): a list of sample_ids from the database
        Returns:
            None:
                Just a print statement saying that it has been successfully submitted
        """
        data = self._post(
            "sample/annotation",
            {
                "annotation_id": annotation_id,
                "sample_ids": sample_ids,
                "retrieve": True,
            },
            expect_data=True,
        )["response"]["data"]
        return data

    def gene_count(self, sample_ids):
        """Get gene TPMs

        Get read counts for all pre-quantified genes in a sample

        Args:
            sample_ids (int, list):  one or more sample ids

        Examples:
            >>> # p is a logged in portal session
            >>> p.gene_count([33, 48])

        Returns:
            DataFrame:
                table of read counts with sample ids as column names and gene names
                as row names
        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        counts = self._post(
            "sample/TPM",
            {
                "sample_ids": sample_ids,
                "minimal": True,
                "raw_counts": True,
                "pseudocounts": 0,
            },
            expect_data=True,
        )["response"]["data"]
        out = pd.DataFrame.from_dict(counts[0], orient="index").sort_index()
        out.columns = [str(x["sample_id"]) for x in counts[1]]
        return out

    def locus_density(self, sample_ids, locus):
        """Get locus density profile

        Get binned coverage counts for a locus

        Args:
            sample_ids (int, [int]):  one or more sample ids
            locus(str): locus in the form "chr:start-stop"

        Examples:
            >>> # p is a logged in portal session
            >>> p.locus_density(33, "chr1:1000000-1100000")

        Returns:
            dict(DataFrame):
                dictionary of DataFrames containing RPK normalized mean signal
                per bin with one value per strand. One entry in the dictionary
                per sample being queried.
        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        density = self._post(
            "density/locus",
            {"sample_ids": sample_ids, "locus": locus},
            expect_data=True,
        )["response"]["data"]
        out = {}
        # Iterate over all returned values (2 per sample, one for each strand) and
        # place them in a dictionary of DataFrames where the key is the sample id
        for entry in density:
            id = str(entry["ID"])
            x = pd.DataFrame.from_dict(entry["values"])
            x["strand"] = entry["strand"]
            if id not in out:
                out[id] = x
            else:
                out[id] = pd.concat([out[id], x])
        for k in out.keys():
            out[k].columns = ["bin_center", "value", "strand"]
        return out

    def download_fastq(self, sample_ids, target_directory="."):
        """Download fastq

        Download the fastq file(s) associated with the sample id(s)

        Args:
            sample_ids (int, [int]):  one or more sample ids
            target_directory(str): path to directory where files should be downloaded
                to. Will be created if it does not exist

        Examples:
            >>> # p is a logged in portal session
            >>> p.download_fastq(33, "./my_project/fastq")

        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        os.makedirs(target_directory, exist_ok=True)
        types = ["fastq", "fastq2"]
        urls = {}
        for i in sample_ids:
            for t in types:
                filesize = self._post(
                    f"fileSize/sample/{t}/{i}",
                    {
                        "ignoreProject": 1,
                    },
                )["response"]["data"]
                if filesize > 0:
                    read_suffix = "R1" if t == "fastq" else "R2"
                    filepath = os.path.join(
                        target_directory, f"{i}_{read_suffix}.fastq.gz"
                    )
                    urls[filepath] = self._post(
                        f"download/sample/{t}/{i}",
                        {
                            "ignoreProject": 1,
                        },
                    )["response"]["data"]
        _download(urls)

    def download_bam(self, sample_ids, target_directory="."):
        """Download bam

        Download the bam file(s) associated with the sample id(s)

        Args:
            sample_ids (int, [int]):  one or more sample ids
            target_directory(str): path to directory where files should be downloaded
                to. Will be created if it does not exist

        Examples:
            >>> # p is a logged in portal session
            >>> p.download_bam(33, "./my_project/bam")

        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        os.makedirs(target_directory, exist_ok=True)
        urls = {}
        for i in sample_ids:
            filesize = self._post(f"fileSize/sample/bam/{i}", {"ignoreProject": 1})[
                "response"
            ]["data"]
            if filesize > 0:
                filepath = os.path.join(target_directory, f"{i}.bam")
                urls[filepath] = self._post(
                    f"download/sample/bam/{i}",
                    {
                        "ignoreProject": 1,
                    },
                )["response"]["data"]
        _download(urls)

    def sample_pipeline_info(self, sample_ids, get_config=False):
        """Get processing pipeline information about sample(s)

        Args:
            sample_ids (int, [int]):  one or more sample ids
            get_config (bool): whether to retrieve the full configuration for each
                processing pipeline

         Returns:
            {sample_id:{configuration}}: dictionary associating each sample id with
                a dictionary of configurations
        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        data = self._post(
            "sample/pipeline_info",
            {"sample_ids": sample_ids, "retrieve_config": int(get_config)},
            expect_data=True,
        )["response"]["data"]
        out = {i: j for i, j in zip(sample_ids, data)}
        return out

    def _is_stranded(self, sample_ids):
        """Get stranded/unstranded status

        Get whether  associated with the sample id(s)

        Args:
            sample_ids (int, [int]):  one or more sample ids

         Returns:
            {sample_id:bool}: dictionary associating each sample id with a boolean value,
            True if stranded.
        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        data = self._post(
            "sample/is_stranded",
            {
                "sample_ids": sample_ids,
            },
            expect_data=True,
        )["response"]["data"]
        out = {i: j for i, j in zip(sample_ids, data)}
        return out

    def download_bigwig(self, sample_ids, target_directory="."):
        """Download bigwig

        Download the bigwig file(s) associated with the sample id(s)

        Args:
            sample_ids (int, [int]):  one or more sample ids
            target_directory(str): path to directory where files should be downloaded
                to. Will be created if it does not exist

        Examples:
            >>> # p is a logged in portal session
            >>> p.download_bigwig(33, "./my_project/bigwig")

        """
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]
        sample_ids = _list_to_int_list(sample_ids)
        os.makedirs(target_directory, exist_ok=True)
        # Dictionary of the file types to use for both stranded and unstranded data
        suffix_dict = {
            "stranded": {
                "bigwigPos": "pos.normalized.bw",
                "bigwigNeg": "neg.normalized.bw",
            },
            "unstranded": {"bigwig": "normalized.bw"},
        }
        # get sample info
        stranded = self._is_stranded(sample_ids=sample_ids)
        urls = {}
        for i in sample_ids:
            filesize = self._post(f"fileSize/sample/bigwig/{i}", {"ignoreProject": 1})[
                "response"
            ]["data"]
            is_stranded = stranded[i]
            str_key = "stranded" if is_stranded else "unstranded"
            for t in suffix_dict[str_key].keys():
                if filesize > 0:
                    suffix = suffix_dict[str_key][t]
                    filepath = os.path.join(target_directory, f"{i}.{suffix}")
                    urls[filepath] = self._post(
                        f"download/sample/{t}/{i}",
                        {
                            "ignoreProject": 1,
                        },
                    )["response"]["data"]
        _download(urls)
