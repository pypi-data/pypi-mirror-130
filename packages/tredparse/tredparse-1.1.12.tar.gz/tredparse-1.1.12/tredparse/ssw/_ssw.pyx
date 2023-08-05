# cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

"""
@package ssw_wrap
@brief Simple python wrapper for SSW align library
To use the dynamic library libssw.so you may need to modify the LD_LIBRARY_PATH environment
variable to include the library directory (export LD_LIBRARY_PATH=$PWD) or for definitive
inclusion of the lib edit /etc/ld.so.conf and add the path or the directory containing the
library and update the cache by using /sbin/ldconfig as root
@copyright  [The MIT licence](http://opensource.org/licenses/MIT)
@author     Clement & Adrien Leger - 2014
"""

# ~~~~~~~GLOBAL IMPORTS~~~~~~~#
# Standard library packages
from libc.stdint cimport int8_t, int32_t, uint8_t, uint16_t, uint32_t
from cpython.mem cimport PyMem_Malloc, PyMem_Free


cdef extern from "ssw.h":
    ctypedef struct _profile:
        pass
    ctypedef _profile s_profile
    ctypedef struct s_align:
        uint16_t score1
        uint16_t score2
        int32_t ref_begin1
        int32_t ref_end1
        int32_t read_begin1
        int32_t read_end1
        int32_t ref_end2
        uint32_t *cigar
        int32_t cigarLen

    s_profile *ssw_init(
        const int8_t *read,
        const int32_t readLen,
        const int8_t *mat,
        const int32_t n,
        const int8_t score_size
    )
    void init_destroy(s_profile *p)
    s_align *ssw_align(
        const s_profile *prof,
        const int8_t *ref,
        int32_t refLen,
        const uint8_t weight_gapO,
        const uint8_t weight_gapE,
        const uint8_t flag,
        const uint16_t filters,
        const int32_t filterd,
        const int32_t maskLen
    )
    void align_destroy(s_align *a)
    char cigar_int_to_op(uint32_t cigar_int)
    uint32_t cigar_int_to_len(uint32_t cigar_int)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
cdef class Aligner:
    """
    @class  SSWAligner
    @brief Wrapper for SSW align library
    """

    cdef int8_t mat[25]
    cdef int8_t *_ref_seq

    cdef public:
        int gap_extend, gap_open, match, mismatch
        bint report_cigar, report_secondary
        object ref_seq

    # Dictionary to map Nucleotide to int as expected by the SSW C library
    base_to_int = {
        "A": 0,
        "C": 1,
        "G": 2,
        "T": 3,
        "N": 4,
        "a": 0,
        "c": 1,
        "g": 2,
        "t": 3,
        "n": 4,
    }
    int_to_base = {0: "A", 1: "C", 2: "G", 3: "T", 4: "N"}

    # ~~~~~~~ FUNDAMENTAL METHODS ~~~~~~~#

    def __repr__(self):
        msg = self.__str__()
        msg += "SCORE PARAMETERS:\n"
        msg += " Gap Weight     Open: {}     Extension: {}\n".format(
            -self.gap_open, -self.gap_extend
        )
        msg += " Align Weight   Match: {}    Mismatch: {}\n\n".format(
            self.match, -self.mismatch
        )
        msg += " Match/mismatch Score matrix\n"
        msg += " \tA\tC\tG\tT\tN\n"
        msg += " A\t{}\t{}\t{}\t{}\t{}\n".format(
            self.match, -self.mismatch, -self.mismatch, -self.mismatch, 0
        )
        msg += " C\t{}\t{}\t{}\t{}\t{}\n".format(
            -self.mismatch, self.match, -self.mismatch, -self.mismatch, 0
        )
        msg += " G\t{}\t{}\t{}\t{}\t{}\n".format(
            -self.mismatch, -self.mismatch, self.match, -self.mismatch, 0
        )
        msg += " T\t{}\t{}\t{}\t{}\t{}\n".format(
            -self.mismatch, -self.mismatch, -self.mismatch, self.match, 0
        )
        msg += " N\t{}\t{}\t{}\t{}\t{}\n\n".format(0, 0, 0, 0, 0)
        msg += "REFERENCE SEQUENCE :\n"
        if len(self.ref_seq) <= 50:
            msg += self.ref_seq + "\n"
        else:
            msg += self.ref_seq[:50] + "...\n"
        msg += " Length: {} nucleotides\n".format(len(self.ref_seq))
        return msg

    def __str__(self):
        return "\n<Instance of {}>\n".format(self.__class__.__name__)

    def __init__(
        self,
        ref_seq="",
        match=2,
        mismatch=2,
        gap_open=3,
        gap_extend=1,
        report_secondary=False,
        report_cigar=False,
    ):
        """
        Initialize object by creating an interface with ssw library fonctions
        A reference sequence is also assigned to the object for multiple alignment against queries
        with the align function
        @param ref_seq Reference sequence as a python string (case insensitive)
        @param match Weight for a match
        @param mismatch Absolute value of mismatch penalty
        @param gap_open Absolute value of gap open penalty
        @param gap_extend Absolute value of gap extend penalty
        @param report_secondary Report the 2nd best alignment if true
        @param report_cigar Report cigar string if true
        """

        # Store overall alignment parameters
        self.report_secondary = report_secondary
        self.report_cigar = report_cigar

        # Set gap penalties
        self.set_gap(gap_open, gap_extend)

        # Set the cost matrix
        self.set_mat(match, mismatch)

        # Set the reference sequence
        self.reference = ref_seq

    def __dealloc__(self):
        """
        Free the memory allocated by the SSW library
        """
        PyMem_Free(self._ref_seq)

    # ~~~~~~~SETTERS METHODS~~~~~~~#

    def set_gap(self, gap_open=3, gap_extend=1):
        """
        Store gapopen and gap extension penalties
        """
        self.gap_open = gap_open
        self.gap_extend = gap_extend

    def set_mat(self, match=2, mismatch=2):
        """
        Store match and mismatch scores then initialize a Cost matrix and fill it with match and
        mismatch values. Ambiguous base: no penalty
        """
        self.match = match
        self.mismatch = mismatch

        # Initialize the cost matrix
        self.mat[:] = [
            match, -mismatch, -mismatch, -mismatch, 0,
            -mismatch, match, -mismatch, -mismatch, 0,
            -mismatch, -mismatch, match, -mismatch, 0,
            -mismatch, -mismatch, -mismatch, match, 0,
            0, 0, 0, 0, 0,
        ]

    @property
    def reference(self):
        return self.ref_seq

    @reference.setter
    def reference(self, ref_seq):
        self.ref_seq = ref_seq
        PyMem_Free(self._ref_seq)
        self._ref_seq = self.dna_to_int_mat(self.ref_seq)

    def align(self, query_seq, min_score=0, min_len=0):
        """
        Perform the alignment of query against the object reference sequence
        @param query_seq Query sequence as a python string (case in-sensitive)
        @param min_score Minimal score of match. None will be return in case of filtering out
        @param min_len Minimal length of match. None will be return in case of filtering out
        @return A SSWAlignRes Object containing information about the alignment.
        """
        # Determine the size of the ref sequence and cast it in a c type integer matrix
        cdef int8_t *_query_seq = self.dna_to_int_mat(query_seq)

        # Create the query profile using the query sequence
        profile = ssw_init(
            _query_seq,  # Query seq in c type integers
            len(query_seq),  # Length of Queryseq in bytes
            self.mat,  # Score matrix
            5,  # Square root of the number of elements in mat
            2,
        )  # flag = no estimation of the best alignment score

        # Setup the mask_len parameters = distance between the optimal and suboptimal alignment
        # if < 15, the function will NOT return the suboptimal alignment information

        if len(query_seq) > 30:
            mask_len = len(query_seq) // 2
        else:
            mask_len = 15

        c_result = ssw_align(
            profile,  # Query profile
            self._ref_seq,  # Ref seq in c type integers
            len(self.ref_seq),  # Length of Refseq in bites
            self.gap_open,  # Absolute value of gap open penalty
            self.gap_extend,  # absolute value of gap extend penalty
            1,  # Bitwise FLAG for output values = return all
            0,  # Score filter = return all
            0,  # Distance filter = return all
            mask_len,
        )  # Distance between the optimal and suboptimal alignment

        # Transform the Cstructure into a python object if score and length match the requirements
        score = c_result.score1
        match_len = c_result.read_end1 - c_result.read_begin1 + 1

        if score >= min_score and match_len >= min_len:
            py_result = make_PyAlignRes(c_result, query_seq, self.ref_seq)
        else:
            py_result = None

        # Free reserved space by ssw.init and ssw_init methods.
        init_destroy(profile)
        align_destroy(c_result)
        PyMem_Free(_query_seq)

        # Return the object
        return py_result

    cdef int8_t *dna_to_int_mat(self, str seq):
        cdef int8_t *query_num = <int8_t *>PyMem_Malloc(len(seq) * sizeof(int8_t))

        # for each letters in ATCGN transform in integers thanks to self.base_to_int
        for (idx, base) in enumerate(seq):
            try:
                value = self.base_to_int[base]
            # if the base is not in the canonic DNA bases assign 4 as for N
            except KeyError:
                value = 4
            finally:
                query_num[idx] = value
        return query_num

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
cdef class PyAlignRes:
    """
    @class  PyAlignRes
    @brief  Extract and verify result from a CAlignRes structure. A comprehensive python
    object is created according to user requirements (+- cigar string and secondary alignment)
    """

    cdef public:
        uint16_t score
        str ref_seq
        int32_t ref_begin
        int32_t ref_end
        str query_seq
        int32_t query_begin
        int32_t query_end

    cdef object _cigar_string

    # ~~~~~~~ FUNDAMENTAL METHOD ~~~~~~~#

    def __str__(self):
        msg = "OPTIMAL MATCH\n"
        msg += "Score            {}\n".format(self.score)
        msg += "Reference begin  {}\n".format(self.ref_begin)
        msg += "Reference end    {}\n".format(self.ref_end)
        msg += "Query begin      {}\n".format(self.query_begin)
        msg += "Query end        {}\n".format(self.query_end)

        if self.cigar_string:
            msg += "Cigar_string     {}\n".format(self.cigar_string)

        return msg

    @property
    def iter_cigar(self):
        for val in self._cigar_string:
            op_len = cigar_int_to_len(val)
            op_char = cigar_int_to_op(val)
            yield op_len, chr(op_char)

    @property
    def cigar_string(self):
        # Empty string for iterative writing of the cigar string
        cigar_string = ""
        if len(self._cigar_string) == 0:
            return cigar_string

        # If the query match do not start at its first base
        # = introduce a softclip at the begining
        if self.query_begin > 0:
            op_len = self.query_begin
            op_char = "S"
            cigar_string += "{}{}".format(op_len, op_char)

        # Iterate over the cigar (pointer to a vector of int)
        cigar_string += "".join("{}{}".format(op_len, op_char) for op_len, op_char in self.iter_cigar)

        # If the length of bases aligned is shorter than the overall query length
        # = introduce a softclip at the end
        end_len = len(self.query_seq) - self.query_end - 1
        if end_len != 0:
            op_len = end_len
            op_char = "S"
            cigar_string += "{}{}".format(op_len, op_char)

        return cigar_string

    @property
    def cigar(self):
        return self.cigar_string

    @property
    def alignment(self):
        def seqiter(seq):
            seq = iter(seq)

            def getseq(cnt):
                return str.join("", [next(seq) for x in range(cnt)])

            return getseq

        r_seq = seqiter(self.ref_seq)
        q_seq = seqiter(self.query_seq)
        r_line = m_line = q_line = ""
        if self.query_begin > 0:  # Soft-clipped
            q_seq(self.query_begin)
        if self.ref_begin > 0:
            r_seq(self.ref_begin)

        for op_len, op_char in self.iter_cigar:
            op_len = int(op_len)
            oc = op_char.upper()
            if oc == "M":
                for (r_base, q_base) in zip(r_seq(op_len), q_seq(op_len)):
                    r_line += r_base
                    q_line += q_base
                    if r_base == q_base:
                        m_line += "|"
                    else:
                        m_line += "*"
            elif oc in "I":
                r_line += "-" * op_len
                m_line += " " * op_len
                q_line += q_seq(op_len)
            elif oc == "D":
                r_line += r_seq(op_len)
                m_line += " " * op_len
                q_line += "-" * op_len
        return r_line, m_line, q_line


cdef make_PyAlignRes(s_align *Res, str query_seq, str ref_seq):
    cdef PyAlignRes b = PyAlignRes.__new__(PyAlignRes)
    b.score = Res.score1
    b.ref_seq = ref_seq
    b.ref_begin = Res.ref_begin1
    b.ref_end = Res.ref_end1
    b.query_seq = query_seq
    b.query_begin = Res.read_begin1
    b.query_end = Res.read_end1
    b._cigar_string = [
        Res.cigar[idx] for idx in range(Res.cigarLen)
    ]
    return b
